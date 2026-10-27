from typing import Any, TypedDict
from urllib.parse import urlsplit

from flask import Blueprint, jsonify, request
from sqlalchemy import select

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

def is_valid_image_url(path: str) -> bool:
    if path.startswith("src/imagesAndFonts/stopsImages/"):
        if any(char in path for char in ("\\", "?", "#")):
            return False
        parts = path.split("/")
        filename = parts[-1].lower()
        allowed_extensions = (".png", ".jpg", ".jpeg")
        return (
            all(part not in ("", ".", "..") for part in parts)
            and filename.endswith(allowed_extensions)
        )
    try:
        parsed = urlsplit(path)
        return (
            parsed.scheme in {"http", "https"}
            and parsed.hostname is not None
            and parsed.port != 0
        )
    except ValueError:
        return False

def check_stop_id(id):
    if isinstance(id, int) and not id < 1:
        if db.session.get(Stop, id) == None:
            return False, ["stop doesn't exist", 404]
        else:
            return True, None
    else:
        return False, ["invalid stop id", 400]

def check_and_extract_stop():
    data: dict[str, Any] = request.get_json(silent=True) or {}
    dataRequirements = {"name": {"type": str, "minChars": 1, "maxChars": 255, "required": True},
                        "wheelchair_accessible": {"type": bool, "required": True},
                        "has_shelter": {"type": bool, "required": True},
                        "has_ticket_machine": {"type": bool, "required": True},
                        "image_url": {"type": str, "maxChars": 255, "required": False, "other_musts": ["validURL"]},
                        }
    for name in data:
        if name not in dataRequirements.keys():
            return False, ("invalid input data", 400)
    for info in dataRequirements:
        if data.get(info) is None:
            if dataRequirements[info]["required"] == False:
                data[info] = None
            else:
                return False, ("invalid input data", 400)
        else:
            if isinstance(data[info], dataRequirements[info]["type"]):
                if dataRequirements[info].get("maxChars") is not None:
                    if len(data[info]) <= dataRequirements[info]["maxChars"]:
                        if dataRequirements[info].get("minChars") is not None:
                            if not len(data[info]) >= dataRequirements[info]["minChars"]:
                                return False, ("invalid input data", 400)
                    else:
                        return False, ("invalid input data", 400)
                if dataRequirements[info].get("other_musts") is not None:
                    for must in dataRequirements[info].get("other_musts"):
                        if must == "validURL":
                            if not is_valid_image_url(data[info]):
                                return False, ("invalid input data", 400)
            else:
                return False, ("invalid input data", 400)

    return True, {"name": data["name"], "image_url": data["image_url"], "wheelchair_accessible": data["wheelchair_accessible"], "has_shelter": data["has_shelter"], "has_ticket_machine": data["has_ticket_machine"]}

def stop_to_dict(stop):
    return {"id": stop.id, "name": stop.name, "image_url": stop.image_url, "wheelchair_accessible":  stop.wheelchair_accessible, "has_shelter": stop.has_shelter, "has_ticket_machine": stop.has_ticket_machine}

@stops_bp.get("")
def list_stops():
    stops = db.session.scalars(select(Stop).order_by(Stop.id)).all()
    return jsonify([stop_to_dict(stop) for stop in stops]), 200

@stops_bp.get("/<stop_id>")
def getStop(stop_id):
    state, data = check_stop_id(stop_id)
    if state == False:
        return jsonify({"message": data[0]}), data[1]
    stop = db.session.get(Stop, stop_id)
    return jsonify(stop_to_dict(stop)), 200

@stops_bp.put("/<stop_id>")
def updateStop(stop_id):
    state, data = check_stop_id(stop_id)
    if state == False:
        return jsonify({"message": data[0]}), data[1]
    stop = db.session.get(Stop, stop_id)
    state, data = check_and_extract_stop()
    if state is False:
        return jsonify({"message": data[0]}), data[1]

    stop.name = data["name"]
    stop.image_url = data["image_url"]
    stop.wheelchair_accessible = data["wheelchair_accessible"]
    stop.has_shelter = data["has_shelter"]
    stop.has_ticket_machine = data["has_ticket_machine"]
    # stop.is_transfer = data["is_transfer"]
    # stop.x = data["x"]
    # stop.y = data["y"]
    db.session.commit()
    return jsonify(stop_to_dict(stop)), 200

@stops_bp.delete("/<stop_id>")
def deleteStop(stop_id):
    state, message = check_stop_id(stop_id)
    if state == False:
        return jsonify({"message": message[0]}), message[1]
    stop = db.session.get(Stop, stop_id)
    db.session.delete(stop)
    db.session.commit()
    return "", 204

@stops_bp.post("")
def createStop():
    state, data = check_and_extract_stop()
    if state is False:
        return jsonify({"message": data[0]}), data[1]
    stop = Stop()
    stop.name = data["name"]
    stop.image_url = data["image_url"]
    stop.wheelchair_accessible = data["wheelchair_accessible"]
    stop.has_shelter = data["has_shelter"]
    stop.has_ticket_machine = data["has_ticket_machine"]
    # stop.is_transfer = data["is_transfer"]
    # stop.x = data["x"]
    # stop.y = data["y"]
    # stop.has_bench = data["has_bench"]
    # stop.has_display = data["has_display"]
    stop.is_transfer = False
    stop.x = 0
    stop.y = 0
    stop.has_bench = False
    stop.has_display = False

    db.session.add(stop)
    db.session.commit()
    
    return stop_to_dict(stop), 201


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
