import datetime

from sqlalchemy import func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Task(Base):
    __abstract__ = True

    run_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


class CurrencyUpdateTask(Task):
    __tablename__ = "currency_update_task"

    rates: Mapped[dict] = mapped_column(JSON)
