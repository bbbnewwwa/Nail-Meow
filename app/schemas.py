from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ========== УСЛУГИ ==========

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    duration: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== ПОЛЬЗОВАТЕЛИ ==========

class UserBase(BaseModel):
    email: str = Field(..., min_length=5, max_length=100)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "client"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== ЗАПИСИ ==========

class BookingBase(BaseModel):
    client_name: str
    client_phone: str
    service_id: int
    appointment_date: str  # ← строка для простоты
    status: str = "pending"
    comment: Optional[str] = None
    master_name: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    client_id: Optional[int] = None
    created_at: str
    
    class Config:
        from_attributes = True