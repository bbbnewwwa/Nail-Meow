from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration: Optional[int] = None
    category: Optional[str] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MasterBase(BaseModel):
    full_name: str
    specialization: Optional[str] = None
    rating: float = 0.0
    description: Optional[str] = None
    is_active: bool = True

class MasterResponse(MasterBase):
    id: int
    
    class Config:
        from_attributes = True

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

class BookingResponse(BookingBase):
    id: int
    client_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True