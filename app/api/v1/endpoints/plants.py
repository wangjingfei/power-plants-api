from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.plant import plant
from app.schemas.plant import Plant, PlantCreate, PlantUpdate, PlantResponse
from app.models.plant import Plant as PlantModel

router = APIRouter()

@router.get("/user", response_model=List[PlantResponse])
def get_user_plants(
    user_id: int = Query(..., description="用户ID"),
    db: Session = Depends(deps.get_db)
):
    """获取指定用户的所有电站"""
    plants = db.query(PlantModel)\
        .filter(PlantModel.owner_id == user_id)\
        .all()
    
    if not plants:
        raise HTTPException(
            status_code=404,
            detail=f"No plants found for user {user_id}"
        )
    
    return plants

@router.get("/city/{city}", response_model=List[Plant])
def read_plants_by_city(
    city: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取特定城市的所有电站"""
    return plant.get_by_city(db, city=city, skip=skip, limit=limit)

@router.get("/status/{status}", response_model=List[Plant])
def read_plants_by_status(
    status: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取特定状态的所有电站"""
    return plant.get_by_status(db, status=status, skip=skip, limit=limit)

@router.get("/account/{account_id}", response_model=List[Plant])
def read_account_plants(
    account_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取特定账户的所有电站"""
    return plant.get_by_account_id(db, account_id=account_id, skip=skip, limit=limit)

@router.get("/owner/{owner_id}", response_model=List[Plant])
def read_owner_plants(
    owner_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取特定用户的所有电站"""
    return plant.get_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)

@router.get("/", response_model=List[Plant])
def read_plants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取所有电站数据"""
    return plant.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Plant)
def create_plant(
    *,
    db: Session = Depends(deps.get_db),
    plant_in: PlantCreate
) -> Any:
    """创建新的电站"""
    existing_plant = plant.get_by_plant_id(db, plant_id=plant_in.plantId)
    if existing_plant:
        raise HTTPException(
            status_code=400,
            detail="The plant with this ID already exists"
        )
    return plant.create(db, obj_in=plant_in)

@router.get("/{plant_id}", response_model=Plant)
def read_plant(
    plant_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """通过ID获取特定电站"""
    db_plant = plant.get(db, id=plant_id)
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db_plant

@router.put("/{plant_id}", response_model=Plant)
def update_plant(
    *,
    db: Session = Depends(deps.get_db),
    plant_id: int,
    plant_in: PlantUpdate
) -> Any:
    """更新电站数据"""
    db_plant = plant.get(db, id=plant_id)
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant.update(db, db_obj=db_plant, obj_in=plant_in)

@router.delete("/{plant_id}", response_model=Plant)
def delete_plant(
    *,
    db: Session = Depends(deps.get_db),
    plant_id: int
) -> Any:
    """删除电站"""
    db_plant = plant.get(db, id=plant_id)
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant.remove(db, id=plant_id) 