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
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service_update: dict):
    service = get_service(db, service_id)
    if service:
        for key, value in service_update.items():
            setattr(service, key, value)
        db.commit()
        db.refresh(service)
    return service

def delete_service(db: Session, service_id: int):
    service = get_service(db, service_id)
    if service:
        db.delete(service)
        db.commit()
    return service

def get_master(db: Session, master_id: int):
    return db.query(models.Master).filter(models.Master.id == master_id).first()

def get_masters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Master).filter(models.Master.is_active == True).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).order_by(models.Booking.appointment_date.desc()).offset(skip).limit(limit).all()