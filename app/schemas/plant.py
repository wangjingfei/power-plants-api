from pydantic import BaseModel, constr
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class PlantBase(BaseModel):
    owner_id: Optional[int] = None
    account_id: Optional[int] = None
    plantId: Optional[constr(max_length=40)] = None
    plantName: Optional[constr(max_length=16)] = None
    createDate: Optional[date] = None
    city: Optional[constr(max_length=16)] = None
    plantAddress: Optional[constr(max_length=32)] = None
    nominalPower: Optional[int] = None
    status: Optional[int] = None
    currentPac: Optional[Decimal] = None
    formulaMoney: Optional[Decimal] = None
    eToday: Optional[Decimal] = None
    eTotal: Optional[Decimal] = None
    etodayMoney: Optional[Decimal] = None
    etotalMoney: Optional[Decimal] = None
    investMoney: Optional[Decimal] = 0
    eMonth: Optional[Decimal] = None
    emonthMoney: Optional[Decimal] = None

class PlantCreate(PlantBase):
    plantId: constr(max_length=40)
    plantName: constr(max_length=16)
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

class PlantResponse(BaseModel):
    id: int
    owner_id: Optional[int] = None
    account_id: Optional[int] = None
    plantId: str
    plantName: str
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
    lastUpdate: Optional[datetime] = None
    investMoney: Optional[Decimal] = 0
    eMonth: Optional[Decimal] = None
    emonthMoney: Optional[Decimal] = None
    
    class Config:
        from_attributes = True 