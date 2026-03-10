from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import services, bookings, admin

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix=f"{settings.API_V1_STR}/services", tags=["Services"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_STR}/bookings", tags=["Bookings"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Nail Meow API is running", "version": settings.VERSION}