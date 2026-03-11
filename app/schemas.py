from pydantic import BaseModel, Field, EmailStr
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
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "client"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

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
    master_id: Optional[int] = None
    master_name: Optional[str] = None
    appointment_date: datetime
    status: str = "pending"
    comment: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    service_id: Optional[int] = None
    master_id: Optional[int] = None
    master_name: Optional[str] = None
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    comment: Optional[str] = None

class BookingResponse(BookingBase):
    id: int
    client_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True