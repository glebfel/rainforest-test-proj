from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.models.orders import OrderItemModel, OrderModel, OrderStatus
from src.db.models.products import ProductModel


class ReportsService:
    def __init__(self, db: Session):
        self.db = db

    def generate_report(self, start_date: datetime, end_date: datetime) -> dict:
        stmt_revenue = select(func.sum(OrderModel.total_price)).where(
            OrderModel.created_at >= start_date,
            OrderModel.created_at <= end_date,
        )
        result_revenue = self.db.execute(stmt_revenue)
        total_revenue = result_revenue.scalar() or 0

        stmt_profit = (
            select(
                func.sum(
                    OrderItemModel.quantity * (ProductModel.price - ProductModel.cost),
                ),
            )
            .join(ProductModel, ProductModel.id == OrderItemModel.product_id)
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(
                OrderModel.created_at >= start_date,
                OrderModel.created_at <= end_date,
            )
        )
        result_profit = self.db.execute(stmt_profit)
        total_profit = result_profit.scalar() or 0

        stmt_units_sold = (
            select(func.sum(OrderItemModel.quantity))
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(
                OrderModel.created_at >= start_date,
                OrderModel.created_at <= end_date,
            )
        )
        result_units_sold = self.db.execute(stmt_units_sold)
        units_sold = result_units_sold.scalar() or 0

        stmt_returns = (
            select(func.sum(OrderItemModel.quantity))
            .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
            .where(
                OrderModel.status == OrderStatus.CANCELLED,
                OrderModel.created_at >= start_date,
                OrderModel.created_at <= end_date,
            )
        )
        result_returns = self.db.execute(stmt_returns)
        returns = result_returns.scalar() or 0

        return {
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "units_sold": units_sold,
            "returns": returns,
        }
