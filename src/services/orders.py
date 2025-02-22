from typing import Dict
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models.orders import OrderModel, OrderItemModel, OrderStatus
from src.db.models.products import ProductModel
from src.schemas.orders import Order, OrderCreate


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: OrderCreate) -> Order:
        async with self.db.begin():
            db_order = OrderModel(
                сustomer_name=order_data.customer_name,
                total_price=order_data.total_price,
            )
            self.db.add(db_order)

            order_items = []

            for item_data in order_data.items:
                stmt = (
                    select(ProductModel)
                    .where(ProductModel.id == item_data.product_id)
                    .with_for_update()
                )
                result = await self.db.execute(stmt)
                product = result.scalars().first()

                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product with id={item_data.product_id} not found"
                    )

                if product.stock < item_data.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for product {product.id}"
                    )

                product.stock -= item_data.quantity

                db_order_item = OrderItemModel(
                    order_id=db_order.id,
                    product_id=product.id,
                    quantity=item_data.quantity,
                    price_at_purchase=product.price
                )
                order_items.append(db_order_item)

            self.db.add_all(order_items)
            db_order.status = OrderStatus.COMPLETED

        stmt = (
            select(OrderModel)
            .where(OrderModel.id == db_order.id)
            .options(selectinload(OrderModel.products))
        )
        result = await self.db.execute(stmt)
        db_order_fresh = result.scalars().first()

        return Order.from_orm(db_order_fresh)

    async def cancel_order(self, order_id: int) -> Dict[str, str]:
        async with self.db.begin():
            stmt_order = select(OrderModel).where(OrderModel.id == order_id)
            result_order = await self.db.execute(stmt_order)
            db_order = result_order.scalars().first()

            if db_order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Order with id={order_id} not found"
                )

            db_order.status = OrderStatus.CANCELLED

            for item in db_order.items:
                stmt_product = (
                    select(ProductModel)
                    .where(ProductModel.id == item.product_id)
                    .with_for_update()
                )
                result_product = await self.db.execute(stmt_product)
                db_product = result_product.scalars().first()
                if db_product:
                    db_product.stock += item.quantity

        return {"message": "Order canceled and returns processed"}
