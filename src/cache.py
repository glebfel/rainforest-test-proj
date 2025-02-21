import hashlib

from redis import Redis, WatchError
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


def generate_cache_key(text: str) -> str:
    """
    Generate a SHA-256 hash key for the given text.
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()