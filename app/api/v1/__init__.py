from fastapi import APIRouter
from app.api.v1.endpoints import daily_reports, users, plants

api_router = APIRouter()
api_router.include_router(daily_reports.router, prefix="/daily-reports", tags=["daily-reports"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(plants.router, prefix="/plants", tags=["plants"])