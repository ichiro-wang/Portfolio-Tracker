from typing import cast
from datetime import date, datetime
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required  # type: ignore

from flasktracker.models import (
    User,
    Portfolio,
    Stock,
    Transaction,
    TransactionType,
    StockWrapper,
)
from flasktracker import db

transactions = Blueprint("transactions", __name__, url_prefix="/api/transactions")
authenticated_user: User = cast(User, current_user)


@transactions.route("/create", methods=["POST"])
@login_required
def create_transaction():
    """
    create a transaction
    requires ticker, type, price, quantity, date
    """
    try:
        data: dict[str, any] = request.json

        # must include portfolio it belongs to
        portfolio_id = int(data.get("portfolioId"))
        if not portfolio_id:
            return jsonify({"error": "No portfolio specified"}), 400

        # check if the portfolio belongs to the current user making the request
        exists = db.session.query(
            db.session.query(Portfolio.id)
            .filter(
                Portfolio.id == portfolio_id,
                Portfolio.owner_id == authenticated_user.id,
            )
            .exists()
        ).scalar()
        if not exists:
            return jsonify({"error": "Invalid request"}), 403

        # check for transaction type (buy, sell)
        type = data.get("type", "").strip().lower()
        if type not in [TransactionType.BUY.value, TransactionType.SELL.value]:
            return jsonify({"error": "Invalid transaction type"}), 400
        type = TransactionType(type)

        # other values from request body
        input_date = data.get("date")
        quantity = float(data.get("quantity", 0))
        price = float(data.get("price", 0))
        ticker: str = data.get("ticker", "").strip().upper()

        # must include these properties
        if not quantity or not price or not ticker or not input_date:
            return jsonify({"error": "Missing data"}), 400
        # validate quantity
        if quantity <= 0:
            return jsonify({"error": "Invalid quantity"}), 400
        # validate price
        if price <= 0:
            return jsonify({"error": "Invalid price"}), 400

        # date comes in as YYYY-MM-DD string
        formatted_date = datetime.strptime(input_date, "%Y-%m-%d")
        # ensure date is not in future
        if formatted_date.date() > date.today():
            return jsonify({"error": "Transaction date cannot be in the future"}), 400

        """
        stock wrapper for caching api call results
        check if one exists, if not, create one
        potential issue with concurrent creation
        """
        stock_wrapper: StockWrapper = (
            db.session.query(StockWrapper).filter(StockWrapper.ticker == ticker).first()
        )
        if not stock_wrapper:
            stock_wrapper = StockWrapper(ticker=ticker)
            db.session.add(stock_wrapper)
            db.session.flush()

        # query for stock in the target portfolio
        stock: Stock = (
            db.session.query(Stock)
            .filter(Stock.ticker == ticker, Stock.portfolio_id == portfolio_id)
            .first()
        )
        if not stock:
            stock = Stock(
                ticker=ticker, wrapper_id=stock_wrapper.id, portfolio_id=portfolio_id
            )
            db.session.add(stock)
            db.session.flush()

        # create new transaction
        transaction = Transaction(
            type=type,
            quantity=quantity,
            price=price,
            stock_id=stock.id,
            date=formatted_date,
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify(transaction.to_json()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in create_transaction: {e}")
        return jsonify({"error": str(e)}), 500


@transactions.route("/<int:id>", methods=["GET"])
@login_required
def get_transaction(id: int):
    """
    retrieve transaction details based on id, belonging to the user
    """
    try:
        transaction: Transaction = db.session.get(Transaction, id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        if transaction.stock.portfolio.owner_id != authenticated_user.id:
            return jsonify({"error": "Invalid request"}), 403

        return jsonify(transaction.to_json())
    except Exception as e:
        return jsonify({"error": str(e)})


@transactions.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_transaction(id: int):
    """
    delete transaction details based on id, belonging to the user
    """
    try:
        data: dict[str, any] = request.json

        # check if portfolio of transaction belongs to current user
        portfolio_id = data.get("portfolioId")
        if not portfolio_id:
            return jsonify({"error": "No portfolio specified"}), 400
        if portfolio_id not in [p.id for p in authenticated_user.portfolios]:
            return jsonify({"error": "Invalid request"}), 403

        # retrieve from db once verified above
        transaction_to_delete = db.session.get(Transaction, id)
        if not transaction_to_delete:
            return jsonify({"error": "Transaction not found"}), 404

        # get stock id for frontend react-query
        stock_id = transaction_to_delete.stock_id

        db.session.delete(transaction_to_delete)
        db.session.commit()

        return jsonify({"deletedId": id, "stockId": stock_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
