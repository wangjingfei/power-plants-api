from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.crud.base import CRUDBase
from app.models.monthly_report import MonthlyReport
from app.schemas.monthly_report import MonthlyReportCreate, MonthlyReportUpdate

class CRUDMonthlyReport(CRUDBase[MonthlyReport, MonthlyReportCreate, MonthlyReportUpdate]):
    def get_by_date_and_user(self, db: Session, *, date: date, user_id: int) -> Optional[MonthlyReport]:
        return db.query(MonthlyReport).filter(
            and_(MonthlyReport.date == date, MonthlyReport.userId == user_id)
        ).first()
    
    def get_by_user_id(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[MonthlyReport]:
        return db.query(MonthlyReport).filter(MonthlyReport.userId == user_id)\
            .order_by(MonthlyReport.date.desc())\
            .offset(skip).limit(limit).all()
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: date, 
        end_date: date, 
        user_id: Optional[int] = None
    ) -> List[MonthlyReport]:
        query = db.query(MonthlyReport)\
            .filter(MonthlyReport.date >= start_date)\
            .filter(MonthlyReport.date <= end_date)
        
        if user_id:
            query = query.filter(MonthlyReport.userId == user_id)
            
        return query.order_by(MonthlyReport.date.desc()).all()

monthly_report = CRUDMonthlyReport(MonthlyReport) 