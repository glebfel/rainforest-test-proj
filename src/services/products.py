from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.products import ProductModel
from src.schemas.products import Product, ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(self, product_data: ProductCreate) -> Product:
        try:
            db_product = ProductModel(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                cost=product_data.cost,
                stock=product_data.stock
            )
            self.db_session.add(db_product)
            await self.db_session.commit()
            await self.db_session.refresh(db_product)
            return Product.from_orm(db_product)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"Product with name '{product_data.name}' already exists")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Product:
        try:
            stmt = select(ProductModel).where(ProductModel.id == product_id)
            result = await self.db_session.execute(stmt)
            db_product = result.scalars().first()
            if db_product is None:
                raise HTTPException(status_code=404, detail="Product not found")

            if product_data.name and db_product.name != product_data.name:
                db_product.name = product_data.name
            if product_data.description and db_product.description != product_data.description:
                db_product.description = product_data.description
            if product_data.price and db_product.price != product_data.price:
                db_product.price = product_data.price
            if product_data.stock and db_product.stock != product_data.stock:
                db_product.stock = product_data.stock
            if product_data.cost and db_product.cost != product_data.cost:
                db_product.cost = product_data.cost

            await self.db_session.commit()
            await self.db_session.refresh(db_product)
            return Product.from_orm(db_product)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"Product with name '{product_data.name}' already exists")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    async def get_products(self, skip: int = 0, limit: int = 10) -> list[Product]:
        stmt = select(ProductModel).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        return [Product.from_orm(product) for product in result.scalars().all()]
