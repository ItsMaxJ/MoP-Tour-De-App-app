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

class Stop(db.Model):
    __tablename__: str = "stops"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_transfer: Mapped[bool] = mapped_column()
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()
    wheelchair_accessible: Mapped[bool] = mapped_column()
    has_shelter: Mapped[bool] = mapped_column()
    has_bench: Mapped[bool] = mapped_column()
    has_ticket_machine: Mapped[bool] = mapped_column()
    has_display: Mapped[bool] = mapped_column()
    
    def to_dict(self) -> dict[str, object]:
        return {"id": self.id,
                "name": self.name,
                "image_url": self.image_url,
                "is_transfer": self.is_transfer,
                "x": self.x,
                "y": self.y,
                "wheelchair_accessible":  self.wheelchair_accessible,
                "has_shelter": self.has_shelter,
                "has_bench": self.has_bench,
                "has_ticket_machine": self.has_ticket_machine,
                "has_display": self.has_display}
