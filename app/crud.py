from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хешировать пароль"""
    return pwd_context.hash(password)

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

def update_service(db: Session, service