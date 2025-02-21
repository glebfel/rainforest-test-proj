from sqlalchemy import MetaData, Column, DateTime
from sqlalchemy.orm import declarative_base

from src.db.utils import utcnow
from src.settings import settings

Base = declarative_base(metadata=MetaData(schema=settings.POSTGRES_SCHEMA))


class DateTimeMixin:
    created_at_utc = Column(DateTime, nullable=False, default=utcnow())
