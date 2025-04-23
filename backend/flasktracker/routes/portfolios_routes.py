from typing import cast
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from flasktracker.models import User, Portfolio
from flasktracker import db

portfolios = Blueprint("portfolios", __name__, url_prefix="/api/portfolios")
authenticated_user: User = cast(User, current_user)


"""
retrieve all portfolios belonging to current user
"""
@portfolios.route("/all", methods=["GET"])
@login_required
def get_all_portfolios():
    try:
        # get portfolios as a list
        ports_json = [
            port.to_json(include_properties=True)
            for port in authenticated_user.portfolios
        ]
        return jsonify(ports_json), 200
    except Exception as e:
        return jsonify({"error": str(e)})


"""
create a portfolio
portfolio requires a name
"""
@portfolios.route("/create", methods=["POST"])
@login_required
def create_portfolio():
    try:
        data: dict[str, str] = request.json
        name = data.get("name", "").strip()

        # name must be in request body
        if not name:
            return jsonify({"error": "No name for portfolio"}), 400

        # create portfolio
        new_portfolio = Portfolio(name=name, owner_id=authenticated_user.id)
        db.session.add(new_portfolio)
        db.session.commit()

        return jsonify(new_portfolio.to_json(include_properties=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


"""
retrieve a portfolio based on id, belonging to the user
"""
@portfolios.route("/<int:id>", methods=["GET"])
@login_required
def get_portfolio(id: int):
    try:
        portfolio: Portfolio = db.session.get(Portfolio, id)
        if not portfolio:
            return jsonify({"error": f"Portfolio with id {id} could not be found"}), 404
        if portfolio.owner_id != authenticated_user.id:
            return jsonify({"error": "Invalid request"}), 403

        # get stocks in the portfolio as a list
        stocks_json = [s.to_json(include_properties=True) for s in portfolio.stocks]

        return (
            jsonify(
                {
                    "portfolio": portfolio.to_json(include_properties=True),
                    "stocks": stocks_json,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500



"""
delete a portfolio based on id, belonging to the user
"""
@portfolios.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_portfolio(id: int):
    try:
        port_to_delete = db.session.get(Portfolio, id)
        if not port_to_delete:
            return jsonify({"error": f"Portfolio with id {id} could not be found"}), 404
        if port_to_delete.owner_id != authenticated_user.id:
            return jsonify({"error": "Invalid request"}), 403

        db.session.delete(port_to_delete)
        db.session.commit()

        return jsonify({"deletedId": id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})


# TODO: update portfolio name
