from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

def get_db() -> Generator:
    """
    数据库依赖项，用于注入数据库会话
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 