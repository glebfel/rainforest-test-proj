from uuid import UUID

from fastapi import APIRouter, Depends, Request

from src.dependencies import get_order_service
from src.schemas.orders import Order, OrderCreate
from src.services.orders import OrderService

orders_router = APIRouter()


@orders_router.post("/")
async def create_order(
    request: Request,
    order: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
) -> Order:
    return await order_service.create_order(order)


@orders_router.post("/{order_id}")
async def cancel_order(
    request: Request,
    order_id: UUID,
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.cancel_order(order_id)
