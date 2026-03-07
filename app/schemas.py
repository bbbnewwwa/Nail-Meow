from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    duration: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MasterBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    specialization: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    photo_url: Optional[str] = None
    schedule: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class MasterCreate(MasterBase):
    pass

class MasterUpdate(BaseModel):
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    photo_url: Optional[str] = None
    schedule: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class MasterResponse(MasterBase):
    id: int
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    client_name: str = Field(..., min_length=2)
    client_phone: str = Field(..., min_length=10)
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

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "client"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ReviewBase(BaseModel):
    service_id: Optional[int] = None
    master_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    discount: float = Field(default=0.0, ge=0.0, le=100.0)
    stock_quantity: int = Field(default=0, ge=0)
    article: Optional[str] = None
    image_url: Optional[str] = None
    characteristics: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    stock_quantity: Optional[int] = None
    article: Optional[str] = None
    image_url: Optional[str] = None
    characteristics: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True