import enum
from decimal import Decimal
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class CurrencyType(enum.Enum):
    FIAT = "fiat"
    CRYPTO = "crypto"


class Currency(Base):
    __tablename__ = "currency"

    name: Mapped[str]
    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    rate: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    type: Mapped[CurrencyType]
