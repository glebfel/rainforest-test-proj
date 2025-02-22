import datetime
import uuid

from sqlalchemy import MetaData, Column, DateTime, UUID
from sqlalchemy.orm import declarative_base

from src.settings import settings

Base = declarative_base(metadata=MetaData(schema=settings.POSTGRES_SCHEMA))


class IdMixin:
    id = Column(UUID, primary_key=True, default=uuid.uuid4)


class DateTimeMixin:
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
