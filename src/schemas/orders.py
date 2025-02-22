from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int


class OrderItem(OrderItemBase):
    id: UUID
    price: Decimal
    order_id: UUID

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: str


class OrderCreate(OrderBase):
    items: list[OrderItemBase]


class Order(OrderBase):
    id: UUID
    items: list[OrderItem]
    status: str
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
