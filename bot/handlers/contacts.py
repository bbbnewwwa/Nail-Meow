from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "contacts")
async def process_contacts(callback: CallbackQuery):
    text = (
        "Контакты Nail Meow\n\n"
        "г. Красноярск, ул. Матросова, 20, каб. 101\n"
        "+7 (999) 123-45-67\n"
        "info@nailmeow.ru\n"
        "Пн-Вс: 10:00 - 21:00"
    )
    await callback.message.answer(text)
    await callback.answer()