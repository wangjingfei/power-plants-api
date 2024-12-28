from fastapi import APIRouter
from app.api.v1.endpoints import daily_reports, monthly_reports, users

api_router = APIRouter()
api_router.include_router(daily_reports.router, prefix="/daily-reports", tags=["daily_reports"])
api_router.include_router(monthly_reports.router, prefix="/monthly-reports", tags=["monthly_reports"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 