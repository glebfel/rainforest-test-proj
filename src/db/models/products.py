from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import validates

from src.db.base import Base, DateTimeMixin, IdMixin


class ProductModel(IdMixin, DateTimeMixin, Base):
    __tablename__ = "products"

    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Numeric, nullable=False)
    cost = Column(Numeric, nullable=False)
    stock = Column(Integer, default=0)

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price must be greater than 0")
        return price

    @validates("cost")
    def validate_cost(self, key, cost):
        if cost < 0:
            raise ValueError("Cost must be greater than 0")
        return cost
