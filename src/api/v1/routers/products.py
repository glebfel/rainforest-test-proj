from uuid import UUID

from fastapi import APIRouter, Depends, Request

from src.cache import cache
from src.services.products import ProductService
from src.dependencies import get_product_service
from src.schemas.products import Product, ProductCreate, ProductUpdate

products_router = APIRouter()


@products_router.post("/")
async def create_product(
        request: Request,
        product: ProductCreate,
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.create_product(product)


@products_router.put("/{product_id}")
async def update_product(
        request: Request,
        product_id: UUID,
        product: ProductUpdate,
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.update_product(product_id, product)


@products_router.get("/")
@cache(ttl_seconds=5)
async def get_products(
        request: Request,
        skip: int = 0,
        limit: int = 10,
        product_service: ProductService = Depends(get_product_service),
) -> list[Product]:
    return await product_service.get_products(skip, limit)
