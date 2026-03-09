from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ServiceResponse])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    services = crud.get_services(db, skip=skip, limit=limit, category=category)
    return services

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service