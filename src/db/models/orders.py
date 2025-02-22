from enum import StrEnum

from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from src.db.base import Base, DateTimeMixin, IdMixin


class OrderStatus(StrEnum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class OrderModel(IdMixin, DateTimeMixin, Base):
    __tablename__ = "orders"

    customer_name = Column(String)
    total_price = Column(Numeric)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    order_items = relationship("OrderItemModel", back_populates="order")


class OrderItemModel(IdMixin, Base):
    __tablename__ = "order_items"

    order_id = Column(UUID, ForeignKey("orders.id"))
    product_id = Column(UUID, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Numeric)

    order = relationship(
        "OrderModel",
        back_populates="order_items",
    )
    product = relationship("ProductModel")
