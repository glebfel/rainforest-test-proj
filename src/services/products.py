from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.products import ProductModel
from src.schemas.products import Product, ProductCreate


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product_data: ProductCreate) -> Product:
        try:
            db_product = ProductModel(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                cost=product_data.cost,
                stock=product_data.stock
            )
            self.db.add(db_product)
            await self.db.commit()
            await self.db.refresh(db_product)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f'Product with name "{product_data.name}" already exists')

        return Product.from_orm(db_product)

    async def update_product(self, product_id: UUID, product_data: ProductCreate) -> Product:
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.db.execute(stmt)
        db_product = result.scalars().first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.price = product_data.price
        db_product.cost = product_data.cost
        db_product.stock = product_data.stock

        await self.db.commit()
        await self.db.refresh(db_product)
        return Product.from_orm(db_product)

    async def get_products(self, skip: int = 0, limit: int = 10) -> list[Product]:
        stmt = select(ProductModel).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [Product.from_orm(product) for product in result.scalars().all()]
