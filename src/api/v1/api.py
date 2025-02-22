from fastapi import APIRouter

from src.api.v1.routers.orders import orders_router
from src.api.v1.routers.products import products_router
from src.api.v1.routers.reports import reports_router

v1_router = APIRouter()

v1_router.include_router(products_router, prefix="/products", tags=["Products"])
v1_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
