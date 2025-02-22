from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates

from src.db.base import Base, DateTimeMixin, IdMixin


class ProductModel(IdMixin, DateTimeMixin, Base):
    __tablename__ = "products"

    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    @validates('price')
    def validate_price(self, key, price):
        assert price >= 0, "Price cannot be negative"
        return price