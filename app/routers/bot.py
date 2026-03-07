from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/link")
async def get_bot_link():
    return {"telegram_bot_link": settings.TELEGRAM_BOT_LINK}