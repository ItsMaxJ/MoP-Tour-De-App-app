from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db
from .routes import product_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # Allow a frontend dev server on another port (e.g. localhost:3000) to call the API.
    CORS(app)

    app.register_blueprint(product_bp, url_prefix="/api/product")

    with app.app_context():
        db.create_all()

    return app
