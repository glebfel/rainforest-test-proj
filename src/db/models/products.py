from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates

from src.db.base import Base, DateTimeMixin


class Product(DateTimeMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    @validates('price')
    def validate_price(self, key, price):
        assert price >= 0, "Price cannot be negative"
        return price

    @validates('cost')
    def validate_cost(self, key, cost):
        assert cost >= 0, "Cost cannot be negative"
        return cost