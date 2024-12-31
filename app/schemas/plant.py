from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class PlantBase(BaseModel):
    owner_id: Optional[int] = None
    account_id: Optional[int] = None
    plantId: Optional[str] = None
    plantName: Optional[str] = None
    createDate: Optional[date] = None
    city: Optional[str] = None
    plantAddress: Optional[str] = None
    nominalPower: Optional[int] = None
    status: Optional[int] = None
    currentPac: Optional[Decimal] = None
    formulaMoney: Optional[Decimal] = None
    eToday: Optional[Decimal] = None
    eTotal: Optional[Decimal] = None
    etodayMoney: Optional[Decimal] = None
    etotalMoney: Optional[Decimal] = None
    investMoney: Optional[Decimal] = None
    eMonth: Optional[Decimal] = None
    emonthMoney: Optional[Decimal] = None

class PlantCreate(PlantBase):
    plantId: str
    plantName: str
    owner_id: int

class PlantUpdate(PlantBase):
    pass

class PlantInDBBase(PlantBase):
    id: int
    lastUpdate: datetime

    class Config:
        from_attributes = True

class Plant(PlantInDBBase):
    pass 