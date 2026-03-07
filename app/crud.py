from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

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

def update_service(db: Session, service_id: int, service: schemas.ServiceUpdate):
    db_service = get_service(db, service_id)
    if db_service:
        update_data = service.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = get_service(db, service_id)
    if db_service:
        db_service.is_active = False
        db.commit()
    return db_service

def get_master(db: Session, master_id: int):
    return db.query(models.Master).filter(models.Master.id == master_id).first()

def get_masters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Master).filter(models.Master.is_active == True).offset(skip).limit(limit).all()

def create_master(db: Session, master: schemas.MasterCreate):
    db_master = models.Master(**master.dict())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def update_master(db: Session, master_id: int, master: schemas.MasterUpdate):
    db_master = get_master(db, master_id)
    if db_master:
        update_data = master.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_master, key, value)
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
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, status: str):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db_booking.status = status
        db.commit()
        db.refresh(db_booking)
    return db_booking

def check_time_slot_available(db: Session, master_id: int, appointment_date: datetime):
    """Проверка, свободно ли время у мастера"""
    existing_booking = db.query(models.Booking).filter(
        models.Booking.master_id == master_id,
        models.Booking.appointment_date == appointment_date,
        models.Booking.status != "cancelled"
    ).first()
    return existing_booking is None

def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(**review.dict(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_service(db: Session, service_id: int):
    return db.query(models.Review).filter(models.Review.service_id == service_id).all()

def get_reviews_for_master(db: Session, master_id: int):
    return db.query(models.Review).filter(models.Review.master_id == master_id).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.is_active == True).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def get_sales_report(db: Session, start_date: datetime, end_date: datetime):
    """Отчет по продажам"""
    bookings = db.query(models.Booking).filter(
        models.Booking.appointment_date.between(start_date, end_date),
        models.Booking.status == "completed"
    ).all()
    return bookings

def get_master_workload(db: Session):
    """Загруженность мастеров"""
    return db.query(
        models.Master.id,
        models.Master.full_name,
        func.count(models.Booking.id).label('booking_count')
    ).join(
        models.Booking, models.Master.id == models.Booking.master_id
    ).group_by(models.Master.id).all()