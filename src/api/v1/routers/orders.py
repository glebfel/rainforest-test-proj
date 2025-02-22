from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status

from services.orders import OrderService
from src.dependencies import get_order_service
from src.schemas.orders import Order, OrderCreate

orders_router = APIRouter()


@orders_router.post("/")
async def create_order(order: OrderCreate, order_service: OrderService = Depends(get_order_service)) -> Order:
    return await order_service.create_order(order)


@orders_router.post("/{order_id}")
async def cancel_order(order_id: UUID, order_service: OrderService = Depends(get_order_service)):
    return await order_service.cancel_order(order_id)
