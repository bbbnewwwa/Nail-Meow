from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    return {
        "services": db.query(models.Service).count(),
        "masters": db.query(models.Master).count(),
        "bookings": db.query(models.Booking).count(),
        "users": db.query(models.User).count()
    }