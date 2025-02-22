from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.api.v1.api import v1_router
from src.lifespan import lifespan
from src.settings import settings


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded. Try again later."
    )


def create_app() -> FastAPI:
    app = FastAPI(title=settings.TITLE, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(v1_router, prefix="/api/v1")

    limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    return app