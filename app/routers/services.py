from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas, models
from app.auth import get_current_admin_user

router = APIRouter()


# ========== PUBLIC ENDPOINTS (для всех пользователей) ==========

@router.get("/", response_model=List[schemas.ServiceResponse])
async def get_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Получить список всех активных услуг с фильтрацией по категории.
    Доступно всем пользователям.
    """
    services = crud.get_services(db, skip=skip, limit=limit, category=category)
    return services


@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить информацию об услуге по ID.
    Доступно всем пользователям.
    """
    service = crud.get_service(db, service_id=service_id)
    if service is None or not service.is_active:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# ========== ADMIN ENDPOINTS (только для менеджера/админа) ==========

@router.post("/", response_model=schemas.ServiceResponse)
async def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Создать новую услугу.
    Доступно только администраторам/менеджерам.
    """
    return crud.create_service(db=db, service=service)


@router.put("/{service_id}", response_model=schemas.ServiceResponse)
async def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Обновить информацию об услуге.
    Доступно только администраторам/менеджерам.
    """
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
    """
    Удалить услугу (мягкое удаление: is_active = False).
    Доступно только администраторам/менеджерам.
    """
    success = crud.delete_service(db=db, service_id=service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}


# ========== ДОПОЛНИТЕЛЬНЫЕ ЭНДПОИНТЫ ==========

@router.get("/category/{category_name}", response_model=List[schemas.ServiceResponse])
async def get_services_by_category(
    category_name: str,
    db: Session = Depends(get_db)
):
    """
    Получить услуги по названию категории.
    Доступно всем пользователям.
    """
    services = crud.get_services(db, category=category_name)
    return services


@router.get("/search", response_model=List[schemas.ServiceResponse])
async def search_services(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    """
    Поиск услуг по названию или описанию.
    Доступно всем пользователям.
    """
    from sqlalchemy import or_
    services = db.query(models.Service).filter(
        models.Service.is_active == True,
        or_(
            models.Service.name.ilike(f"%{q}%"),
            models.Service.description.ilike(f"%{q}%")
        )
    ).all()
    return services