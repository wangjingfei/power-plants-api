from app.models.base import Base
from app.models.user import User
from app.models.account import Account
from app.models.plant import Plant
from app.models.daily_report import DailyReport
from app.models.monthly_report import MonthlyReport

# 这样可以确保所有模型都被正确加载
__all__ = ["Base", "User", "Account", "Plant", "DailyReport", "MonthlyReport"]