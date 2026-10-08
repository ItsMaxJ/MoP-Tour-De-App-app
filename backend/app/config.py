import os
from urllib.parse import quote_plus


class Config:
    FLASK_DB_HOST: str = os.getenv("FLASK_DB_HOST", "localhost")
    FLASK_DB_PORT: str = os.getenv("FLASK_DB_PORT", "3306")
    FLASK_DB_NAME: str = os.getenv("FLASK_DB_NAME", "product")
    FLASK_DB_USER: str = os.getenv("FLASK_DB_USER", "root")
    FLASK_DB_PASSWORD: str = os.getenv("FLASK_DB_PASSWORD", "")

    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{FLASK_DB_USER}:{quote_plus(FLASK_DB_PASSWORD)}"
        f"@{FLASK_DB_HOST}:{FLASK_DB_PORT}/{FLASK_DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
