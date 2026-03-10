from pydantic import BaseModel, Field
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
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
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
    description: Optional[str] = None
    is_active: bool = True

class MasterCreate(MasterBase):
    pass

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

class BookingResponse(BookingBase):
    id: int
    client_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True