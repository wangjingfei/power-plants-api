from sqlalchemy import Column, Integer, String, Date, DECIMAL, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class DailyReport(Base):
    __tablename__ = "daily_report"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    plantId = Column(String(40), ForeignKey("plant.plantId"), nullable=True)
    plantName = Column(String(16), nullable=True)
    plant_owner_id = Column(BigInteger, ForeignKey("user.id"), nullable=True)
    nominalPower = Column(Integer, nullable=True)
    currentPac = Column(DECIMAL(12,2), nullable=True)
    eToday = Column(DECIMAL(12,2), nullable=True)
    etodayMoney = Column(DECIMAL(16,6), nullable=True)
    eTotal = Column(DECIMAL(12,2), nullable=True)
    etotalMoney = Column(DECIMAL(16,6), nullable=True)
    lastUpdate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    eMonth = Column(DECIMAL(12,2), nullable=True)
    emonthMoney = Column(DECIMAL(16,6), nullable=True)

    # 关联关系
    plant = relationship("Plant", back_populates="daily_reports")
    owner = relationship("User", back_populates="daily_reports")