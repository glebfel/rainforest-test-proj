from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import v1_router
from lifespan import lifespan
from src.settings import settings


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

    return app