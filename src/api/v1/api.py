from fastapi import APIRouter

from api.v1.routers.products import products_router

v1_router = APIRouter()

v1_router.include_router(products_router, prefix="/products", tags=["Products"])