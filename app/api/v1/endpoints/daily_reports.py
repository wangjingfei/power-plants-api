from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.daily_report import daily_report
from app.schemas.daily_report import DailyReport, DailyReportCreate, DailyReportUpdate
from datetime import date

router = APIRouter()

@router.get("/", response_model=List[DailyReport])
def read_daily_reports(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    获取所有日报数据
    """
    return daily_report.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=DailyReport)
def create_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: DailyReportCreate
) -> Any:
    """
    创建新的日报数据
    """
    existing_report = daily_report.get_by_date_and_plant(
        db, date=report_in.date, plant_id=report_in.plantId
    )
    if existing_report:
        raise HTTPException(
            status_code=400,
            detail="The daily report for this date and plant already exists"
        )
    return daily_report.create(db, obj_in=report_in)

@router.get("/{report_id}", response_model=DailyReport)
def read_daily_report(
    report_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    通过ID获取特定日报
    """
    db_report = daily_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return db_report

@router.put("/{report_id}", response_model=DailyReport)
def update_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    report_in: DailyReportUpdate
) -> Any:
    """
    更新日报数据
    """
    db_report = daily_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return daily_report.update(db, db_obj=db_report, obj_in=report_in)

@router.delete("/{report_id}", response_model=DailyReport)
def delete_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int
) -> Any:
    """
    删除日报数据
    """
    db_report = daily_report.get(db, id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return daily_report.remove(db, id=report_id)

@router.get("/plant/{plant_id}", response_model=List[DailyReport])
def read_plant_daily_reports(
    plant_id: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    获取特定电站的所有日报数据
    """
    return daily_report.get_by_plant_id(db, plant_id=plant_id, skip=skip, limit=limit)

@router.get("/owner/{owner_id}", response_model=List[DailyReport])
def read_owner_daily_reports(
    owner_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    获取特定用户的所有日报数据
    """
    return daily_report.get_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit) 