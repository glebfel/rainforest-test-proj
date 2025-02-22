from datetime import datetime

from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.services.reports import ReportsService
from src.settings import settings


@shared_task(name="generate_report_task")
def generate_report_task(start_date_str: datetime, end_date_str: datetime) -> dict:
    engine = create_engine(
        (
            f"postgresql://"
            f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
            f"/{settings.POSTGRES_DB}"
        ),
        pool_size=20,
        pool_pre_ping=True,
        pool_use_lifo=True,
    )
    session_factory = sessionmaker(
        engine,
        expire_on_commit=False,
    )
    session = session_factory()
    try:
        reports_service = ReportsService(session)
        return reports_service.generate_report(start_date_str, end_date_str)
    finally:
        session.close()
