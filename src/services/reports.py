from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.reports import Report
from src.db.models.orders import OrderModel, OrderItemModel, OrderStatus
from src.db.models.products import ProductModel


class ReportsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_report(self, start_date: datetime, end_date: datetime) -> Report:
        stmt_revenue = (
            select(func.sum(OrderModel.total_price))
            .where(OrderModel.created_at >= start_date, OrderModel.created_at <= end_date)
        )
        result_revenue = await self.db.execute(stmt_revenue)
        total_revenue = result_revenue.scalar() or 0

        stmt_profit = (
            select(func.sum(OrderItemModel.quantity * (ProductModel.price - ProductModel.cost)))
            .join(ProductModel, ProductModel.id == OrderItemModel.product_id)
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(OrderModel.created_at >= start_date, OrderModel.created_at <= end_date)
        )
        result_profit = await self.db.execute(stmt_profit)
        total_profit = result_profit.scalar() or 0

        stmt_units_sold = (
            select(func.sum(OrderItemModel.quantity))
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(OrderModel.created_at >= start_date, OrderModel.created_at <= end_date)
        )
        result_units_sold = await self.db.execute(stmt_units_sold)
        units_sold = result_units_sold.scalar() or 0

        stmt_returns = (
            select(func.sum(OrderItemModel.quantity))
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(
                OrderModel.status == OrderStatus.CANCELLED,
                OrderModel.created_at >= start_date,
                OrderModel.created_at <= end_date
            )
        )
        result_returns = await self.db.execute(stmt_returns)
        returns = result_returns.scalar() or 0

        return Report(
            total_revenue=total_revenue,
            total_profit=total_profit,
            units_sold=units_sold,
            returns=returns
        )
