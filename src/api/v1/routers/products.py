from uuid import UUID

from fastapi import APIRouter, Depends

from services.products import ProductService
from src.dependencies import get_product_service
from src.schemas.products import Product, ProductCreate

products_router = APIRouter()


@products_router.post("/")
async def create_product(
        product: ProductCreate,
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.create_product(product)


@products_router.put("/{product_id}")
async def update_product(
        product_id: UUID,
        product: ProductCreate,
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.update_product(product_id, product)


@products_router.get("/")
async def get_products(
        skip: int = 0,
        limit: int = 10,
        product_service: ProductService = Depends(get_product_service),
) -> list[Product]:
    return await product_service.get_products(skip, limit)
