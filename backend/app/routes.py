from typing import Any, TypedDict

from flask import Blueprint, jsonify, request
from sqlalchemy import select, delete

from .extensions import db
from .models import Product, Team

product_bp = Blueprint("products", __name__)
team_bp = Blueprint("team", __name__)

@team_bp.post("/create")
def saveTeam():
	data = request.get_json(silent=True)
	name = data.get("teamName")
	team = data.get("teammates")
	if not isinstance(name, str) or not isinstance(team, list):
		return jsonify("invalid input"), 400
	
	teamInfo = Team(teamName=name, teammates=team)
	db.session.add(teamInfo)
	db.session.commit()
	
	return jsonify(teamInfo.id), 201

@team_bp.get("")
def getTeam():
	teams = db.session.scalars(select(Team).order_by(Team.id)).all()
	return jsonify([team.to_dict() for team in teams]), 200

@team_bp.delete("")
def delTeams():
  db.session.execute(delete(Team))
  db.session.commit()
  return jsonify("success"), 200


class ProductData(TypedDict):
	name: str
	cost: int


def extract_product() -> ProductData | None:
	data: dict[str, Any] = request.get_json(silent=True) or {}  # pyright: ignore[reportExplicitAny]
	if data.get("name") is None or data.get("cost") is None:
		return None

	return {"name": data["name"], "cost": data["cost"]}

@product_bp.get("")
def list_products():
	products = db.session.scalars(select(Product).order_by(Product.id)).all()
	return jsonify([product.to_dict() for product in products]), 200


@product_bp.post("")
def create_product():
	data = extract_product()
	if data is None:
		return jsonify({"message": "name and cost are required"}), 400

	product = Product()
	product.name = data["name"]
	product.cost = data["cost"]
	db.session.add(product)
	db.session.commit()

	return jsonify(product.to_dict()), 200


@product_bp.put("/<int:product_id>")
def update_product(product_id: int):
	product = db.session.get(Product, product_id)
	if product is None:
		return jsonify({"message": "Product does not exist"}), 404

	data = extract_product()
	if data is None:
		return jsonify({"message": "name and cost are required"}), 400

	product.name = data["name"]
	product.cost = data["cost"]
	db.session.commit()

	return jsonify(product.to_dict()), 200


@product_bp.delete("/<int:product_id>")
def delete_product(product_id: int):
	product = db.session.get(Product, product_id)
	if product is not None:
		db.session.delete(product)
		db.session.commit()

	return jsonify({"message": "Product was deleted permanently from DB."}), 200
