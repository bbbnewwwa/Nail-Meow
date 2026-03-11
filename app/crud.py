from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from passlib.context import CryptContext

# ========== УСЛУГИ (SERVICE) ==========

def get_service(db: Session, service_id: int):
    """Получить услугу по ID"""
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    """Получить список услуг с фильтрацией"""
    query = db.query(models.Service).filter(models.Service.is_active == True)
    if category:
        query = query.filter(models.Service.category == category)
    return query.offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate):
    """Создать новую услугу"""
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service_update: schemas.ServiceUpdate):
    """Обновить услугу (частичное обновление)"""
    service = get_service(db, service_id)
    if not service:
        return None
    
    update_data = service_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)
    
    db.commit()
    db.refresh(service)
    return service

def delete_service(db: Session, service_id: int):
    """Удалить услугу"""
    service = get_service(db, service_id)
    if service:
        db.delete(service)
        db.commit()
    return service

def get_services_count(db: Session):
    """Получить количество услуг"""
    return db.query(models.Service).count()

# ========== ПОЛЬЗОВАТЕЛИ (USER) ==========

def get_user(db: Session, user_id: int):
    """Получить пользователя по ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Получить пользователя по email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получить список пользователей"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя"""
    from app.auth import get_password_hash
    hashed_password = get_password_hash(user.password)
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

def get_users_count(db: Session):
    """Получить количество пользователей"""
    return db.query(models.User).count()

# ========== ЗАПИСИ (BOOKING) ==========

def get_booking(db: Session, booking_id: int):
    """Получить запись по ID"""
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    """Получить список записей с фильтрацией по статусу"""
    query = db.query(models.Booking)
    if status:
        query = query.filter(models.Booking.status == status)
    return query.order_by(models.Booking.appointment_date.desc()).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    """Создать новую запись"""
    try:
        print(f"📝 Создание записи: {booking.dict()}")
        
        # Конвертируем строку даты в datetime для БД
        from datetime import datetime
        appointment_date = datetime.fromisoformat(booking.appointment_date)
        
        # Создаём запись ТОЛЬКО с теми полями, которые есть в модели
        db_booking = models.Booking(
            client_name=booking.client_name,
            client_phone=booking.client_phone,
            service_id=booking.service_id,
            appointment_date=appointment_date,
            status=booking.status or "pending",
            comment=booking.comment,
            master_name=booking.master_name
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        print(f"✅ Запись создана: {db_booking.id}")
        return db_booking
        
    except Exception as e:
        print(f"❌ Ошибка при создании записи: {e}")
        db.rollback()
        raise

def update_booking(db: Session, booking_id: int, booking_update: dict):
    """Обновить запись"""
    booking = get_booking(db, booking_id)
    if booking:
        for key, value in booking_update.items():
            setattr(booking, key, value)
        db.commit()
        db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    """Удалить запись"""
    booking = get_booking(db, booking_id)
    if booking:
        db.delete(booking)
        db.commit()
    return booking

def get_bookings_count(db: Session):
    """Получить количество записей"""
    return db.query(models.Booking).count()

def get_bookings_by_date(db: Session, date: str):
    """Получить записи по дате"""
    return db.query(models.Booking).filter(
        models.Booking.appointment_date >= date
    ).all()

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хешировать пароль"""
    return pwd_context.hash(password)