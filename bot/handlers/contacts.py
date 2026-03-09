from aiogram import Router, F
from aiogram.types import CallbackQuery
import aiohttp
from config import settings
from keyboards.inline import get_services_keyboard, get_back_keyboard

router = Router()

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    await callback.answer("Загрузка услуг...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.API_URL}/api/services/") as response:
                if response.status == 200:
                    services = await response.json()
                    
                    text = "💅 Наши услуги:\n\n"
                    for service in services[:10]:
                        text += f"**{service['name']}**\n"
                        text += f"{service['price']}₽\n"
                        text += f"⏱ {service['duration']} мин\n"
                        if service.get('description'):
                            text += f"{service['description']}\n"
                        text += "\n"
                    
                    await callback.message.edit_text(
                        text,
                        reply_markup=get_services_keyboard(services),
                        parse_mode="Markdown"
                    )
                else:
                    await callback.message.edit_text(
                        "Не удалось загрузить услуги",
                        reply_markup=get_back_keyboard()
                    )
    except Exception as e:
        await callback.message.edit_text(
            f"Ошибка: {str(e)}",
            reply_markup=get_back_keyboard()
        )
    
    await callback.answer()