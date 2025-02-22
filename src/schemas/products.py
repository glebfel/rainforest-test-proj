from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int = 0


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
