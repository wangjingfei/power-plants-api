from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base

class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=True)
    email = Column(String(64), nullable=True)
    isActive = Column(Boolean, nullable=True)

    # 关联关系
    plants = relationship("Plant", back_populates="account") 