import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings

from handlers import start, services, booking, my_bookings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(services.router)
    dp.include_router(booking.router)
    dp.include_router(my_bookings.router)
    
    print("Бот Nail Meow запущен...")
    print(f"API URL: {settings.API_URL}")
    print("Для остановки нажмите Ctrl+C")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())