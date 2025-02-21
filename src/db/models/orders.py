from enum import StrEnum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.db.base import Base, DateTimeMixin


class OrderStatus(StrEnum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class Order(DateTimeMixin, Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    products = relationship("Product", secondary="order_items")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="products")
    product = relationship("Product")
