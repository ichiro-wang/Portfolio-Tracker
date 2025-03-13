from typing import cast
from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from flasktracker.models import User, Stock
from flasktracker import db

stocks = Blueprint("stocks", __name__, url_prefix="/api/stocks")
authenticated_user: User = cast(User, current_user)


@stocks.route("/<int:id>", methods=["GET"])
@login_required
def get_stock_transactions(id: int):
    try:
        stock: Stock = db.session.get(Stock, id)
        if not stock:
            return jsonify({"error": "Stock with given id not found"}), 404
        if stock.portfolio.owner_id != authenticated_user.id:
            return jsonify({"error": "Invalid request"}), 400

        transactions_json = [t.to_json() for t in stock.transactions]

        return jsonify(transactions_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
