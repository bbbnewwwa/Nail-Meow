from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import get_main_menu

router = Router()

START_TEXT = """
Добро пожаловать в Nail Meow!

Мы рады видеть вас в нашем салоне красоты!

Наши услуги:
- Маникюр и педикюр
- Покрытие гель-лак
- Дизайн ногтей
- SPA-уход

Мы находимся:
г. Красноярск, ул. Матросова, 20, каб. 101

Режим работы:
Ежедневно с 10:00 до 21:00

Выберите действие в меню
"""

HELP_TEXT = """
Помощь

Услуги и цены - посмотреть весь прайс
Записаться - онлайн запись на услугу
Мои записи - просмотр ваших записей
Контакты - как с нами связаться

Как записаться:
1. Нажмите "Записаться"
2. Выберите услугу
3. Выберите дату и время
4. Введите ваше имя и телефон
5. Подтвердите запись

Если у вас остались вопросы, напишите нам!
"""

CONTACTS_TEXT = """
Наши контакты:

Адрес:
г. Красноярск, ул. Матросова, 20, каб. 101

Телефон:
+7 (999) 123-45-67

Email:
info@nailmeow.ru

Сайт:
http://127.0.0.1:8000

Режим работы:
Пн-Вс: 10:00 - 21:00

Telegram бот:
@nailmeow_bot
"""

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        START_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        HELP_TEXT,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            START_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    except Exception as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            HELP_TEXT,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            CONTACTS_TEXT,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()