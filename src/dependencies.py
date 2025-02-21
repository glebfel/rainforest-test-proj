from typing import AsyncGenerator

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()
    try:
        yield session
    finally:
        await session.close()


def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis_client