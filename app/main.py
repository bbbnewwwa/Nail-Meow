from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import services, bookings, admin, bot
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nail Meow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(bot.router, prefix="/api/bot", tags=["Bot"])

@app.get("/")
async def root():
    return {"message": "Nail Meow API is running", "version": "1.0.0"}