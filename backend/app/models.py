from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db


class Product(db.Model):
    __tablename__: str = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "name": self.name, "cost": self.cost}

class Team(db.Model):
    __tablename__: str = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teamName: Mapped[str] = mapped_column(String(100), nullable=False)
    teammates: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "teamName": self.teamName,
            "teammates": self.teammates,
        }
