from typing import AsyncGenerator

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.orders import OrderService
from src.services.products import ProductService


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()
    try:
        yield session
    finally:
        await session.close()


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_order_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(db)
