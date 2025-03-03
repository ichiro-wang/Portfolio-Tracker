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
current_user: User = current_user


@transactions.route("/create", methods=["POST"])
@login_required
def create_transaction():
    try:
        data = request.json

        portfolio_id = data.get("portfolioId")
        if not portfolio_id:
            return jsonify({"error": "No portfolio specified"}), 400

        if portfolio_id not in [p.id for p in current_user.portfolios]:
            return jsonify({"error": "Invalid request"}), 400

        type = data.get("type", "").strip()
        if type not in [TransactionType.BUY.value, TransactionType.SELL.value]:
            return jsonify({"error": "Invalid transaction type"}), 400
        type = TransactionType(type)

        quantity = data.get("quantity")
        price = data.get("price")
        ticker: str = data.get("ticker", "").strip().upper()

        if not quantity or not price or not ticker:
            return jsonify({"error": "Missing data"}), 400

        stock_wrapper: StockWrapper = (
            db.session.query(StockWrapper).filter(StockWrapper.ticker == ticker).first()
        )
        if not stock_wrapper:
            new_wrapper = StockWrapper(ticker=ticker)
            stock_wrapper = new_wrapper
            db.session.add(new_wrapper)
            db.session.flush()

        stock: Stock = db.session.query(Stock).filter(Stock.ticker == ticker).first()
        if not stock:
            new_stock = Stock(
                ticker=ticker, wrapper_id=stock_wrapper.id, portfolio_id=portfolio_id
            )
            stock = new_stock
            db.session.add(new_stock)
            db.session.flush()

        transaction = Transaction(
            type=type, quantity=quantity, price=price, stock_id=stock.id
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify(transaction.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@transactions.route("/<int:id>", methods=["GET"])
@login_required
def get_transaction(id: int):
    try:
        transaction: Transaction = db.session.query(Transaction, id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        if transaction.stock.portfolio.owner_id != current_user.id:
            return jsonify({"error": "Invalid request"}), 400

        return jsonify(transaction.to_json())
    except Exception as e:
        return jsonify({"error": str(e)})
