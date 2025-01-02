from sqlalchemy import Column, Integer, String, Date, DECIMAL, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Plant(Base):
    __tablename__ = "plant"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey("user.id"))
    account_id = Column(BigInteger, ForeignKey("account.id"))
    plantId = Column(String(40), unique=True)
    plantName = Column(String(16))
    createDate = Column(Date)
    city = Column(String(16))
    plantAddress = Column(String(32))
    nominalPower = Column(Integer)
    status = Column(Integer)
    currentPac = Column(DECIMAL(12,2))
    formulaMoney = Column(DECIMAL(14,4))
    eToday = Column(DECIMAL(12,2))
    eTotal = Column(DECIMAL(12,2))
    etodayMoney = Column(DECIMAL(16,6))
    etotalMoney = Column(DECIMAL(16,6))
    lastUpdate = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    investMoney = Column(DECIMAL(16,6), server_default='0.000000')
    eMonth = Column(DECIMAL(12,2))
    emonthMoney = Column(DECIMAL(16,6))

    # 关联关系
    owner = relationship("User", back_populates="plants")
    account = relationship("Account", back_populates="plants")
    daily_reports = relationship("DailyReport", back_populates="plant")