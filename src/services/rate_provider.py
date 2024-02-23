from decimal import Decimal
from typing import Any, Protocol

from db.models import Currency, CurrencyType, CurrencyUpdateTask
from iso4217 import Currency as ISOCurrency
from repositories.currency import CurrencyRepository
from settings import rates_settings
from sqlalchemy.ext.asyncio import AsyncSession


class RateProvider(Protocol):
    async def update_rates(self, session: AsyncSession, rates: dict[str, Any]) -> None:
        raise NotImplemented


class ExchangeRatesAPI(RateProvider):
    async def update_rates(self, session: AsyncSession, response_dict: dict[str, Any]) -> None:
        only_rates: dict[str, float] = response_dict["rates"]
        mapped_currencies = []
        for k, v in only_rates.items():
            try:
                mapped_currencies.append(
                    Currency(code=k, name=ISOCurrency(k).currency_name, rate=Decimal(v), type=CurrencyType.FIAT)
                )
            except ValueError:
                mapped_currencies.append(Currency(code=k, name=k, rate=Decimal(v), type=CurrencyType.CRYPTO))
        currency_repo = CurrencyRepository(session=session)
        if not (currencies := await currency_repo.get_all_currencies()):
            await currency_repo.bulk_create(mapped_currencies)
        else:
            updated_currencies = map(
                lambda x: Currency(
                    code=x.code, name=x.name, type=x.type, rate=Decimal(only_rates.get(x.code) or x.rate)
                ),
                currencies,
            )

            await currency_repo.bulk_update(list(updated_currencies))

        session.add(CurrencyUpdateTask(rates=only_rates))
        await session.commit()


def get_rate_provider() -> type[RateProvider]:
    match rates_settings.api_provider_name:
        case "exchangeratesapi":
            return ExchangeRatesAPI

    raise NotImplemented
