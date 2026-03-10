from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import get_main_menu

router = Router()

START_TEXT = """
Добро пожаловать в Nail Meow!

📍 Адрес:
г. Красноярск, ул. Матросова, 20, каб. 101

⏰ Режим работы:
Ежедневно с 10:00 до 21:00

Нажмите кнопку "Контакты" для связи с нами
"""

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=get_main_menu())

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    text = (
        "Контакты Nail Meow\n\n"
        "Адрес:\n"
        "г. Красноярск, ул. Матросова, 20, каб. 101\n\n"
        "Телефон:\n"
        "+7 (999) 123-45-67\n\n"
        "Email:\n"
        "info@nailmeow.ru\n\n"
        "Сайт:\n"
        "http://127.0.0.1:8000\n\n"
        "Режим работы:\n"
        "Пн-Вс: 10:00 - 21:00"
    )
    await callback.message.answer(text)
    await callback.answer()