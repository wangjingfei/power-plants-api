from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.monthly_report import monthly_report
from app.schemas.monthly_report import MonthlyReport, MonthlyReportCreate, MonthlyReportUpdate
from datetime import date

router = APIRouter()

@router.get("/", response_model=List[MonthlyReport])
def read_monthly_reports(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    获取所有月报数据
    """
    return monthly_report.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=MonthlyReport)
def create_monthly_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: MonthlyReportCreate
) -> Any:
    """
    创建新的月报数据
    """
    existing_report = monthly_report.get_by_date_and_user(
        db, date=report_in.date, user_id=report_in.userId
    )
    if existing_report:
        raise HTTPException(
            status_code=400,
            detail="The monthly report for this date and user already exists"
        )
    return monthly_report.create(db, obj_in=report_in)

@router.get("/{report_id}", response_model=MonthlyReport)
def read_monthly_report(
    report_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    通过ID获取特定月报
    """
    db_report = monthly_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Monthly report not found")
    return db_report

@router.put("/{report_id}", response_model=MonthlyReport)
def update_monthly_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    report_in: MonthlyReportUpdate
) -> Any:
    """
    更新月报数据
    """
    db_report = monthly_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Monthly report not found")
    return monthly_report.update(db, db_obj=db_report, obj_in=report_in)

@router.delete("/{report_id}", response_model=MonthlyReport)
def delete_monthly_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int
) -> Any:
    """
    删除月报数据
    """
    db_report = monthly_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Monthly report not found")
    return monthly_report.remove(db, id=report_id)

@router.get("/user/{user_id}", response_model=List[MonthlyReport])
def read_user_monthly_reports(
    user_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    获取特定用户的所有月报数据
    """
    return monthly_report.get_by_user_id(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/date-range/", response_model=List[MonthlyReport])
def read_date_range_reports(
    start_date: date,
    end_date: date,
    user_id: Optional[int] = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    获取指定日期范围内的月报数据
    """
    return monthly_report.get_by_date_range(
        db, 
        start_date=start_date, 
        end_date=end_date, 
        user_id=user_id
    )