from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.crud.base import CRUDBase
from app.models.daily_report import DailyReport
from app.schemas.daily_report import DailyReportCreate, DailyReportUpdate

class CRUDDailyReport(CRUDBase[DailyReport, DailyReportCreate, DailyReportUpdate]):
    def get_by_date_and_plant(self, db: Session, *, date: date, plant_id: str) -> Optional[DailyReport]:
        return db.query(DailyReport).filter(
            and_(DailyReport.date == date, DailyReport.plantId == plant_id)
        ).first()
    
    def get_by_plant_id(self, db: Session, *, plant_id: str, skip: int = 0, limit: int = 100) -> List[DailyReport]:
        return db.query(DailyReport).filter(DailyReport.plantId == plant_id)\
            .order_by(DailyReport.date.desc())\
            .offset(skip).limit(limit).all()
    
    def get_by_owner_id(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[DailyReport]:
        return db.query(DailyReport).filter(DailyReport.plant_owner_id == owner_id)\
            .order_by(DailyReport.date.desc())\
            .offset(skip).limit(limit).all()

daily_report = CRUDDailyReport(DailyReport) 