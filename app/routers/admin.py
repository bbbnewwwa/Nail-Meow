from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas
from app.auth import get_current_admin_user
from app import models
from datetime import datetime

router = APIRouter()

@router.get("/services/all")
async def admin_get_all_services(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Получить все услуги (включая неактивные)"""
    return db.query(models.Service).all()

@router.post("/masters", response_model=schemas.MasterResponse)
async def admin_create_master(
    master: schemas.MasterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Создать нового мастера"""
    return crud.create_master(db=db, master=master)

@router.put("/masters/{master_id}", response_model=schemas.MasterResponse)
async def admin_update_master(
    master_id: int,
    master: schemas.MasterUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Обновить информацию о мастере"""
    updated_master = crud.update_master(db=db, master_id=master_id, master=master)
    if updated_master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return updated_master

@router.get("/reports/sales")
async def get_sales_report(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Отчет по продажам за период"""
    bookings = crud.get_sales_report(db, start_date, end_date)
    total_revenue = sum(booking.service.price for booking in bookings if hasattr(booking, 'service'))
    return {
        "period": {"start": start_date, "end": end_date},
        "total_bookings": len(bookings),
        "total_revenue": total_revenue,
        "bookings": bookings
    }

@router.get("/reports/master-workload")
async def get_master_workload(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Отчет по загруженности мастеров"""
    return crud.get_master_workload(db)

@router.post("/products", response_model=schemas.ProductResponse)
async def admin_create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Создать новый товар"""
    return crud.create_product(db=db, product=product)

@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
async def admin_update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Обновить информацию о товаре"""
    updated_product = crud.update_product(db=db, product_id=product_id, product=product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product