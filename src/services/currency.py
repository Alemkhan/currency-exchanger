from decimal import Decimal

from api.v1.schemas.rates import ConvertMoneyRequest
from core.exceptions import SpecifiedCurrencyDoesntExists
from db.models import Currency, CurrencyUpdateTask
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class CurrencyService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_rates_last_update_date(self) -> CurrencyUpdateTask | None:
        stmt = select(CurrencyUpdateTask).order_by(desc(CurrencyUpdateTask.run_at))
        row = (await self._session.execute(stmt)).first()
        if not row:
            return None

        return row[0]

    async def convert_money(self, request_body: ConvertMoneyRequest) -> Decimal:
        stmt = select(Currency).where(Currency.code.in_(request_body.currencies))
        rows = (await self._session.execute(stmt)).scalars().all()
        if len(rows) != 2:
            query_result = [row.code for row in rows] + request_body.currencies
            raise SpecifiedCurrencyDoesntExists(currency=list(set(query_result)))
        if rows[0].code == request_body.target:
            target, source = rows[0], rows[1]
        else:
            target, source = rows[1], rows[0]
        if "EUR" in request_body.currencies:
            if target.code == "EUR":
                converted_amount = request_body.amount * source.rate
            else:
                converted_amount = request_body.amount / target.rate
        else:
            cross_currency_convert_rate = source.rate / target.rate
            converted_amount = request_body.amount * cross_currency_convert_rate

        return converted_amount.quantize(Decimal(".000000"))
