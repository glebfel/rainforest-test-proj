import functools
import json
from typing import Any, Callable

from pydantic import BaseModel
from redis import WatchError
from redis.asyncio.client import Redis
from redis.backoff import FullJitterBackoff
from redis.retry import Retry

from src.settings import settings

retry = Retry(FullJitterBackoff(4, 1), retries=3)

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    retry=retry,
    retry_on_error=[WatchError],
)


def cache(ttl_seconds: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key_parts = (
                [func.__name__]
                + list(map(str, args))
                + [f"{k}={v}" for k, v in kwargs.items()]
            )
            cache_key = "cache:" + ":".join(key_parts)

            cached_data = await redis_client.get(cache_key)
            if cached_data is not None:
                return json.loads(cached_data)

            result = await func(*args, **kwargs)

            def serialize_item(item):
                if isinstance(item, BaseModel):
                    return item.model_dump()
                return item

            if isinstance(result, list):
                to_store = [serialize_item(item) for item in result]
            elif isinstance(result, BaseModel):
                to_store = result.model_dump()
            else:
                to_store = result

            await redis_client.setex(
                name=cache_key,
                time=ttl_seconds,
                value=json.dumps(to_store, default=str),
            )
            return result

        return wrapper

    return decorator
