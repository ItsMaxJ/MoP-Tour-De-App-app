from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .extensions import db
from .routes import product_bp, stops_bp
from .seed_stops import seedStops


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # Allow a frontend dev server on another port (e.g. localhost:3000) to call the API.
    CORS(app)

    app.register_blueprint(product_bp, url_prefix="/api/product")
    app.register_blueprint(stops_bp, url_prefix="/api/v1/stops")

    Migrate(app, db)

    @app.cli.command("seed_stops")
    def seed_stops_command():
        seedStops()

    return app
