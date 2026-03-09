from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    query = db.query(models.Service).filter(models.Service.is_active == True)
    if category:
        query = query.filter(models.Service.category == category)
    return query.offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_master(db: Session, master_id: int):
    return db.query(models.Master).filter(models.Master.id == master_id).first()

def get_masters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Master).filter(models.Master.is_active == True).offset(skip).limit(limit).all()

def create_master(db: Session, master: schemas.MasterCreate):
    db_master = models.Master(**master.model_dump())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(models.Booking)
    if status:
        query = query.filter(models.Booking.status == status)
    return query.order_by(models.Booking.appointment_date.desc()).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking