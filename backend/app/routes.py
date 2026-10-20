from typing import Any, TypedDict

from flask import Blueprint, jsonify, request
from sqlalchemy import select, delete

from .extensions import db
from .models import Product, Stops

product_bp = Blueprint("products", __name__)
stops_bp = Blueprint("stops", __name__)

@stops_bp.get("")
def list_stops():
    stops = db.session.scalars(select(Stops).order_by(Stops.id)).all()
    print(stops)
    return jsonify([stop.to_dict() for stop in stops]), 200

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
