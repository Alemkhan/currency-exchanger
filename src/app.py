import traceback
from typing import Any

from api.router import api_router
from asyncpg.exceptions._base import PostgresError
from core.exceptions import ExchangeServiceException, handle_exchange_service_error
from db.session import engine
from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from fastapi.requests import Request
from settings import app_settings
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import text
from starlette import status
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response


def create_app() -> FastAPI:
    app_configuration: dict[str, Any] = {
        "title": app_settings.title,
        "root_path": app_settings.root_path,
    }
    if not app_settings.debug:
        app_configuration.update({"docs_url": None, "redoc_url": None})

    app = FastAPI(**app_configuration)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthcheck")
    async def healthcheck() -> JSONResponse:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except (ConnectionRefusedError, PostgresError):
            return JSONResponse(
                {"status": "db connection failed"},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except DatabaseError:
            return JSONResponse(
                {"status": "db is down"},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)

    app.include_router(api_router, prefix="/api")
    app.add_exception_handler(ExchangeServiceException, handle_exchange_service_error)  # type: ignore

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException) -> Response:
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        return await http_exception_handler(request, exc)

    return app
