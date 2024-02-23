from typing import Sequence

from db.models import Currency
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CurrencyRepository:
    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def get_all_currencies(self) -> Sequence[Currency]:
        return (await self._session.execute(select(Currency))).scalars().all()

    async def get_by_currency_code(self, *, currency_code: str) -> Currency:
        stmt = select(Currency).where(Currency.code == currency_code)
        return (await self._session.execute(stmt)).scalar_one()

    async def bulk_create(self, currencies: list[Currency]) -> None:
        await self._session.run_sync(lambda session: session.bulk_save_objects(currencies))

    async def bulk_update(self, currencies: list[Currency]) -> None:
        await self._session.execute(
            update(Currency), [{"code": currency.code, "rate": currency.rate} for currency in currencies]
        )
