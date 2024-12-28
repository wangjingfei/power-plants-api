from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class DailyReportBase(BaseModel):
    date: Optional[date] = None
    plantId: Optional[str] = None
    plantName: Optional[str] = None
    plant_owner_id: Optional[int] = None
    nominalPower: Optional[int] = None
    currentPac: Optional[Decimal] = None
    eToday: Optional[Decimal] = None
    etodayMoney: Optional[Decimal] = None
    eTotal: Optional[Decimal] = None
    etotalMoney: Optional[Decimal] = None
    eMonth: Optional[Decimal] = None
    emonthMoney: Optional[Decimal] = None

class DailyReportCreate(DailyReportBase):
    pass

class DailyReportUpdate(DailyReportBase):
    pass

class DailyReportInDBBase(DailyReportBase):
    id: int
    lastUpdate: datetime

    class Config:
        from_attributes = True

class DailyReport(DailyReportInDBBase):
    pass 