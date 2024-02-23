from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Currency


class CurrencyRepository:
    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def get_all_currencies(self) -> Sequence[Currency]:
        return (await self._session.execute(select(Currency))).scalars().all()

    async def get_by_currency_code(self, *, currency_code: str) -> Currency:
        stmt = select(Currency).where(Currency.code == currency_code)
        return (await self._session.execute(stmt)).scalar_one()

    async def bulk_create(self, currencies: list[Currency]):
        await self._session.run_sync(lambda session: session.bulk_insert_mappings(Currency, currencies))
        await self._session.commit()
