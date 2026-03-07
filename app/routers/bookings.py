from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app import crud, schemas
from app.auth import get_current_user, get_current_active_user
from app import models

router = APIRouter()

@router.get("/", response_model=List[schemas.BookingResponse])
async def get_bookings(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Получить список записей"""
    if current_user.role == "client":
        # Клиент видит только свои записи
        return []  # Здесь нужно добавить фильтрацию по user_id
    else:
        # Админ/менеджер видит все записи
        return crud.get_bookings(db, skip=skip, limit=limit, status=status)

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Получить информацию о записи"""
    booking = crud.get_booking(db, booking_id=booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/", response_model=schemas.BookingResponse)
async def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Создать новую запись"""
    # Проверка доступности времени
    if booking.master_id:
        is_available = crud.check_time_slot_available(
            db, 
            master_id=booking.master_id, 
            appointment_date=booking.appointment_date
        )
        if not is_available:
            raise HTTPException(
                status_code=400, 
                detail="This time slot is already booked"
            )
    
    return crud.create_booking(db=db, booking=booking)

@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
async def update_booking_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Обновить статус записи"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=403, 
            detail="Only managers can update booking status"
        )
    
    booking = crud.update_booking_status(db=db, booking_id=booking_id, status=status)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking