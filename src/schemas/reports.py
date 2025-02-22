from decimal import Decimal

from pydantic import BaseModel


class Report(BaseModel):
    total_revenue: Decimal
    total_profit: Decimal
    units_sold: int
    returns: int
