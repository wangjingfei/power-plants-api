from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class MonthlyReportBase(BaseModel):
    date: Optional[date] = None
    userId: int
    userName: str
    eToday: Decimal
    etodayMoney: Decimal
    eMonth: Decimal
    emonthMoney: Decimal
    eTotal: Decimal
    etotalMoney: Decimal
    totalNominalPower: int
    totalInvest: Decimal

class MonthlyReportCreate(MonthlyReportBase):
    pass

class MonthlyReportUpdate(MonthlyReportBase):
    pass

class MonthlyReportInDBBase(MonthlyReportBase):
    id: int
    lastUpdate: datetime

    class Config:
        from_attributes = True

class MonthlyReport(MonthlyReportInDBBase):
    pass