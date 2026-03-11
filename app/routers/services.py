from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ServiceResponse])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список всех услуг с фильтрацией по категории"""
    services = crud.get_services(db, skip=skip, limit=limit, category=category)
    return services

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Получить информацию об одной услуге по ID"""
    service = crud.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.post("/", response_model=schemas.ServiceResponse)
async def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):
    """Создать новую услугу"""
    return crud.create_service(db=db, service=service)

@router.patch("/{service_id}", response_model=schemas.ServiceResponse)
async def update_service(
    service_id: int,
    service_update: schemas.ServiceUpdate,
    db: Session = Depends(get_db)
):
    """Обновить услугу (можно изменить только отдельные поля)"""
    service = crud.update_service(db, service_id=service_id, service_update=service_update)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.delete("/{service_id}")
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Удалить услугу по ID"""
    service = crud.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    
    crud.delete_service(db, service_id=service_id)
    return {"message": "Услуга успешно удалена", "id": service_id}