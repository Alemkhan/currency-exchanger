from typing import Any

from fastapi.responses import ORJSONResponse
from starlette import status


class ExchangeServiceException(Exception):
    def __init__(
        self,
        code: str,
        message: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__()
        self.code = code
        self.message = message
        self.status_code = status_code


async def handle_exchange_service_error(_: Any, exc: ExchangeServiceException) -> ORJSONResponse:
    return ORJSONResponse(
        content={"code": exc.code, "message": exc.message},
        status_code=exc.status_code,
    )


class SpecifiedCurrencyDoesntExists(ExchangeServiceException):
    def __init__(self, currency: list[str]) -> None:
        super().__init__(
            code="currency_doesnt_exists",
            message=f"Specified currencies don't exist {','.join(currency)}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
