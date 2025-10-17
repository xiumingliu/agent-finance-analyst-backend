from fastapi import APIRouter
from .v1_health import router as health_router
from .v1_kpi import router as kpi_router
from .v1_series import router as series_router
from .v1_chat import router as chat_router

api_v1 = APIRouter()
api_v1.include_router(health_router, tags=["health"])
api_v1.include_router(kpi_router, tags=["kpi"])
api_v1.include_router(series_router, tags=["series"])
api_v1.include_router(chat_router, tags=["chat"])