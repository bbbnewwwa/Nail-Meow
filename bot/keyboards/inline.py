from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="Услуги и цены", callback_data="services"),
    )
    builder.row(
        InlineKeyboardButton(text="Записаться", callback_data="booking"),
    )
    builder.row(
        InlineKeyboardButton(text="Мои записи", callback_data="my_bookings"),
    )
    builder.row(
        InlineKeyboardButton(text="Контакты", callback_data="contacts"),
        InlineKeyboardButton(text="Помощь", callback_data="help"),
    )
    
    return builder.as_markup()

def get_services_keyboard(services: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for service in services[:10]:
        builder.row(
            InlineKeyboardButton(
                text=f"{service['name']} - {service['price']}₽",
                callback_data=f"service_{service['id']}"
            )
        )
    
    builder.row(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return builder.as_markup()