from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db


class Product(db.Model):
    __tablename__: str = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "name": self.name, "cost": self.cost}
