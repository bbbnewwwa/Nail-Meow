from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas
from app.auth import get_current_admin_user
from app import models

router = APIRouter()

@router.get("/", response_model=List[schemas.ServiceResponse])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список всех услуг"""
    services = crud.get_services(db, skip=skip, limit=limit, category=category)
    return services

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Получить информацию об услуге по ID"""
    service = crud.get_service(db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.post("/", response_model=schemas.ServiceResponse)
async def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Создать новую услугу (только для админов)"""
    return crud.create_service(db=db, service=service)

@router.put("/{service_id}", response_model=schemas.ServiceResponse)
async def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Обновить информацию об услуге (только для админов)"""
    updated_service = crud.update_service(db=db, service_id=service_id, service=service)
    if updated_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return updated_service

@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Удалить услугу (только для админов)"""
    success = crud.delete_service(db=db, service_id=service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}