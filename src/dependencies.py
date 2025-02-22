from typing import AsyncGenerator

from fastapi import Request, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from services.orders import OrderService
from services.products import ProductService
from services.reports import ReportsService


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


def get_reports_service(db: AsyncSession = Depends(get_db)) -> ReportsService:
    return ReportsService(db)


def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis_client
