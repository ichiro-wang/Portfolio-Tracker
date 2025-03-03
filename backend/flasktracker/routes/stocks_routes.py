from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required  # type: ignore

from flasktracker.models import User, Portfolio, Stock, Transaction
from flasktracker import db

stocks = Blueprint("stocks", __name__, url_prefix="/api/stocks")
current_user: User = current_user


@stocks.route("/<int:id>", methods=["GET"])
@login_required
def get_stock(id: int):
    try:
        stock: Stock = db.session.query(Stock, id)
        if not stock:
            return jsonify({"error": "Stock with given id not found"}), 404
        if stock.portfolio.owner_id != current_user.id:
            return jsonify({"error": "Invalid request"}), 400

        transactions_json = [t.to_json() for t in stock.transactions]

        return jsonify(
            {
                "stock": stock.to_json(include_properties=True),
                "transactions": transactions_json,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
