from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: UUID
    order_id: UUID
    quantity: int


class OrderItem(OrderItemBase):
    id: UUID
    price: Decimal

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_name: str
    total_price: Decimal
    status: str


class OrderCreate(OrderBase):
    items: list[OrderItemBase]


class Order(OrderBase):
    id: UUID
    items: list[OrderItem]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
