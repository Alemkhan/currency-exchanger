import datetime
from decimal import Decimal

from core.schemas import BaseSchema


class LastUpdateResponse(BaseSchema):
    last_updated: datetime.datetime


class ConvertMoneyRequest(BaseSchema):
    target: str
    source: str
    amount: Decimal

    @property
    def currencies(self) -> list[str]:
        return [self.target, self.source]


class ConvertMoneyResponse(BaseSchema):
    converted_amount: Decimal
