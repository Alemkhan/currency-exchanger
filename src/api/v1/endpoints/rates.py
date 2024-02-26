import typing

import httpx
from db.dependencies import get_session
from fastapi import APIRouter, Depends, Response
from fastapi.responses import ORJSONResponse
from services.currency import CurrencyService
from services.rate_provider import get_rate_provider
from settings import rates_settings
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas.rates import (
    ConvertMoneyRequest,
    ConvertMoneyResponse,
    LastUpdateResponse,
)

if typing.TYPE_CHECKING:
    from db.models import CurrencyUpdateTask

rates_router = APIRouter(
    tags=["rates"],
    default_response_class=ORJSONResponse,
)


@rates_router.get("/rates-last-update-date")
async def rates_last_update_date(
    session: AsyncSession = Depends(get_session),
) -> LastUpdateResponse | None:
    currency_service = CurrencyService(session)
    last_updated_date: CurrencyUpdateTask | None = await currency_service.get_rates_last_update_date()
    if not last_updated_date:
        return None

    return LastUpdateResponse(last_updated=last_updated_date.run_at)


@rates_router.post("/convert-money")
async def convert_money(
    request_body: ConvertMoneyRequest,
    session: AsyncSession = Depends(get_session),
) -> ConvertMoneyResponse:
    currency_service = CurrencyService(session)
    converted_money = await currency_service.convert_money(request_body)
    return ConvertMoneyResponse(converted_amount=converted_money)


@rates_router.post("/update")
async def update_rates_manually(
    session: AsyncSession = Depends(get_session),
) -> Response:
    async with httpx.AsyncClient() as client:
        data = await client.get(url=rates_settings.api_request_url)
        json_data = data.json()
        rate_provider = get_rate_provider()
        await rate_provider().update_rates(session, json_data)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
