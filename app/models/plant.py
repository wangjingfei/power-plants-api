from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base

class Plant(Base):
    __tablename__ = "plant"

    plantId = Column(String(40), primary_key=True)
    plantName = Column(String(16), nullable=True)
    nominalPower = Column(Integer, nullable=True)
    owner_id = Column(BigInteger, nullable=True)

    # 关联关系
    daily_reports = relationship("DailyReport", back_populates="plant") 