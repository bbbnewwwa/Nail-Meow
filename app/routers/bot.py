from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/link")
async def get_telegram_bot_link():
    """Получить ссылку на Telegram бота"""
    return {
        "telegram_bot_link": settings.TELEGRAM_BOT_LINK,
        "message": "Перейдите по ссылке для связи с нами в Telegram"
    }

@router.get("/info")
async def get_bot_info():
    """Информация о боте"""
    return {
        "bot_name": "Nail Meow Bot",
        "description": "Наш Telegram бот для быстрой записи и уведомлений",
        "features": [
            "Быстрая запись на услуги",
            "Напоминания о записи",
            "Ответы на частые вопросы",
            "Акции и скидки"
        ]
    }