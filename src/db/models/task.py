import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Task(Base):
    __abstract__ = True

    run_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(), server_default=func.now()
    )


class CurrencyUpdateTask(Task):
    __tablename__ = "currency_update_task"

    id: Mapped[UUID] = mapped_column(
        init=False,
        default_factory=uuid4,
        primary_key=True,
    )
    rates: Mapped[dict] = mapped_column(JSON, default_factory=dict)
