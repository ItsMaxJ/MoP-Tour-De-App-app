from typing import Any, TypedDict

from flask import Blueprint, jsonify, request
from sqlalchemy import select, delete

from .extensions import db
from .models import Product, Stop

product_bp = Blueprint("products", __name__)
stops_bp = Blueprint("stops", __name__)

class StopData(TypedDict):
    name: str
    image_url: str
    wheelchair_accessible: bool
    has_shelter: bool
    has_ticket_machine: bool
    is_transfer: bool
    x: float
    y: float
    has_bench: bool
    has_display: bool

def extract_stop() -> StopData | None:
    data: dict[str, Any] = request.get_json(silent=True) or {}
    if data.get("name") is None or data.get("image_url") is None or data.get("wheelchair_accessible") is None or data.get("has_shelter") is None or data.get("has_ticket_machine") is None or data.get("is_transfer") is None or data.get("x") is None or data.get("y") is None or data.get("has_bench") is None or data.get("has_display") is None:
        return None
    return {"name": data["name"], "image_url": data["image_url"], "wheelchair_accessible": data["wheelchair_accessible"], "has_shelter": data["has_shelter"], "has_ticket_machine": data["has_ticket_machine"], "is_transfer": data["is_transfer"], "x": data["x"], "y": data["y"], "has_bench": data["has_bench"], "has_display": data["has_display"]}

@stops_bp.get("")
def list_stops():
    stops = db.session.scalars(select(Stop).order_by(Stop.id)).all()
    return jsonify([stop.to_dict() for stop in stops]), 200

@stops_bp.get("/<int:stop_id>")
def getStop(stop_id: int):
    stop = db.session.get(Stop, stop_id)
    if stop is None:
        return jsonify({"message": "stop doesn't exist"}), 404
    return jsonify(stop.to_dict()), 200

@stops_bp.put("/<int:stop_id>")
def updateStop(stop_id: int):
    stop = db.session.get(Stop, stop_id)
    if stop is None:
        return jsonify({"message": "stop doesn't exist"}), 404
    data = extract_stop()
    if data is None:
        return jsonify({"message": "Invalid stop data"}), 400

    stop.name = data["name"]
    stop.image_url = data["image_url"]
    stop.wheelchair_accessible = data["wheelchair_accessible"]
    stop.has_shelter = data["has_shelter"]
    stop.has_ticket_machine = data["has_ticket_machine"]
    stop.is_transfer = data["is_transfer"]
    stop.x = data["x"]
    stop.y = data["y"]
    db.session.commit()
    return jsonify(stop.to_dict()), 200

@stops_bp.delete("/<int:stop_id>")
def deleteStop(stop_id: int):
    stop = db.session.get(Stop, stop_id)
    if stop is None:
        return jsonify({"message": "stop doesn't exist"}), 404
    db.session.delete(stop)
    db.session.commit()
    return jsonify(""), 204

@stops_bp.post("")
def createStop():
    data = extract_stop()
    if data is None:
        return jsonify({"message": "Invalid stop data"}), 400
    stop = Stop()
    stop.name = data["name"]
    stop.image_url = data["image_url"]
    stop.wheelchair_accessible = data["wheelchair_accessible"]
    stop.has_shelter = data["has_shelter"]
    stop.has_ticket_machine = data["has_ticket_machine"]
    stop.is_transfer = data["is_transfer"]
    stop.x = data["x"]
    stop.y = data["y"]
    stop.has_bench = data["has_bench"]
    stop.has_display = data["has_display"]

    db.session.add(stop)
    db.session.commit()
    
    return stop.to_dict(), 201


class ProductData(TypedDict):
	name: str
	cost: int

def extract_product() -> ProductData | None:
	data: dict[str, Any] = request.get_json(silent=True) or {}
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
