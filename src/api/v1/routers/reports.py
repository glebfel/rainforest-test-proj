from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.reports import Report
from src.services.reports import ReportsService
from src.dependencies import get_reports_service

reports_router = APIRouter()


@reports_router.get("/")
async def generate_report(
    start_date: datetime,
    end_date: datetime,
    reports_service: ReportsService = Depends(get_reports_service),
) -> Report:
    return await reports_service.generate_report(start_date, end_date)
