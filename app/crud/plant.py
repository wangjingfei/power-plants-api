from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.crud.base import CRUDBase
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantUpdate

class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    def get_by_plant_id(self, db: Session, *, plant_id: str) -> Optional[Plant]:
        return db.query(Plant).filter(Plant.plantId == plant_id).first()
    
    def get_by_owner_id(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Plant]:
        return db.query(Plant).filter(Plant.owner_id == owner_id)\
            .offset(skip).limit(limit).all()
    
    def get_by_account_id(self, db: Session, *, account_id: int, skip: int = 0, limit: int = 100) -> List[Plant]:
        return db.query(Plant).filter(Plant.account_id == account_id)\
            .offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, status: int, skip: int = 0, limit: int = 100) -> List[Plant]:
        return db.query(Plant).filter(Plant.status == status)\
            .offset(skip).limit(limit).all()
    
    def get_by_city(self, db: Session, *, city: str, skip: int = 0, limit: int = 100) -> List[Plant]:
        return db.query(Plant).filter(Plant.city == city)\
            .offset(skip).limit(limit).all()

plant = CRUDPlant(Plant) 