from sqlalchemy import Column, Integer, String, Date, DECIMAL, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class DailyReport(Base):
    __tablename__ = "daily_report"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date)
    plantId = Column(String(40), ForeignKey("plant.plantId"))
    plantName = Column(String(16))
    plant_owner_id = Column(BigInteger, ForeignKey("user.id"))
    nominalPower = Column(Integer)
    currentPac = Column(DECIMAL(12,2))
    eToday = Column(DECIMAL(12,2))
    etodayMoney = Column(DECIMAL(16,6))
    eTotal = Column(DECIMAL(12,2))
    etotalMoney = Column(DECIMAL(16,6))
    lastUpdate = Column(TIMESTAMP, default=datetime.utcnow)
    eMonth = Column(DECIMAL(12,2))
    emonthMoney = Column(DECIMAL(16,6))

    # 关联关系
    plant = relationship("Plant", back_populates="daily_reports")
    owner = relationship("User", back_populates="daily_reports")