from sqlalchemy import Column, Integer, String, Date, DECIMAL, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class MonthlyReport(Base):
    __tablename__ = "monthly_report"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    userId = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    userName = Column(String(32), nullable=False)
    eToday = Column(DECIMAL(12,2), nullable=False)
    etodayMoney = Column(DECIMAL(16,6), nullable=False)
    eMonth = Column(DECIMAL(12,2), nullable=False)
    emonthMoney = Column(DECIMAL(16,6), nullable=False)
    eTotal = Column(DECIMAL(12,2), nullable=False)
    etotalMoney = Column(DECIMAL(16,6), nullable=False)
    totalNominalPower = Column(Integer, nullable=False)
    totalInvest = Column(DECIMAL(16,6), nullable=False)
    lastUpdate = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)

    # 关联关系
    user = relationship("User", back_populates="monthly_reports")