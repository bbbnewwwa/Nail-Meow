import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings

from handlers import start, contacts

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(contacts.router)
    
    print("Бот Nail Meow запущен...")
    print(f"API URL: {settings.API_URL}")
    print("Для остановки нажмите Ctrl+C")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())