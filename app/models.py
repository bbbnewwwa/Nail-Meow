from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration = Column(Integer)
    category = Column(String(50))
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="service")

class Master(Base):
    __tablename__ = "masters"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    rating = Column(Float, default=0.0)
    photo_url = Column(String(255))
    schedule = Column(Text)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="master")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    role = Column(String(20), default="client")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="client")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_name = Column(String(100), nullable=False)
    client_phone = Column(String(20), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    master_id = Column(Integer, ForeignKey("masters.id"), nullable=True)
    master_name = Column(String(100))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    master = relationship("Master", back_populates="bookings")