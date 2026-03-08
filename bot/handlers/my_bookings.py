from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_back_keyboard

router = Router()

@router.callback_query(F.data == "my_bookings")
async def show_my_bookings(callback: CallbackQuery):
    text = "Мои записи\n\n"
    text += "Здесь будут ваши активные записи.\n\n"
    text += "Для просмотра записей:\n"
    text += "Используйте наш сайт: http://127.0.0.1:8000\n"
    text += "Или свяжитесь с нами по телефону\n\n"
    text += "(Функция в разработке)\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()