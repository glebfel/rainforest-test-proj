from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.products import ProductModel
from src.schemas.products import Product, ProductCreate


class ProductService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(self, product_data: ProductCreate) -> Product:
        try:
            db_product = ProductModel(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                stock=product_data.stock
            )
            self.db_session.add(db_product)
            await self.db_session.commit()
            await self.db_session.refresh(db_product)
            return Product.from_orm(db_product)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"Product with name '{product_data.name}' already exists")

    async def update_product(self, product_id: UUID, product_data: ProductCreate) -> Product:
        try:
            stmt = select(ProductModel).where(ProductModel.id == product_id)
            result = await self.db_session.execute(stmt)
            db_product = result.scalars().first()
            if db_product is None:
                raise HTTPException(status_code=404, detail="Product not found")

            db_product.name = product_data.name
            db_product.description = product_data.description
            db_product.price = product_data.price
            db_product.stock = product_data.stock

            await self.db_session.commit()
            await self.db_session.refresh(db_product)
            return Product.from_orm(db_product)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"Product with name '{product_data.name}' already exists")

    async def get_products(self, skip: int = 0, limit: int = 10) -> list[Product]:
        stmt = select(ProductModel).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        return [Product.from_orm(product) for product in result.scalars().all()]
