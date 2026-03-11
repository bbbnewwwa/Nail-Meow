from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API роуты
app.include_router(services.router, prefix=f"{settings.API_V1_STR}/services", tags=["Services"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_STR}/bookings", tags=["Bookings"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/services")
async def services_page(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/booking")
async def booking_page(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/contacts")
async def contacts_page(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})

@app.get("/api")
async def api_root():
    return {"message": "Nail Meow API is running", "version": settings.VERSION}