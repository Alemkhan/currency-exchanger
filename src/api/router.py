from fastapi import APIRouter

from .v1.endpoints.rates import rates_router

api_router = APIRouter()
api_router.include_router(rates_router, prefix="/v1/rates")
