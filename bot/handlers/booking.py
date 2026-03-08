from aiogram import Router, F
from aiogram.fsm import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
import aiohttp
from datetime import datetime
from config import settings
from keyboards.inline import get_back_keyboard, get_cancel_keyboard

router = Router()

class BookingState(StatesGroup):
    service = State()
    date = State()
    name = State()
    phone = State()

@router.callback_query(F.data == "booking")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Запись на услугу")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.API_URL}/services/") as response:
                if response.status == 200:
                    services = await response.json()
                    
                    text = "Запись на услугу\n\n"
                    text += "Выберите услугу:\n\n"
                    
                    for i, service in enumerate(services[:10], 1):
                        text += f"{i}. {service['name']} - {service['price']}₽ ({service['duration']} мин)\n"
                    
                    await callback.message.edit_text(
                        text,
                        reply_markup=get_back_keyboard(),
                        parse_mode="Markdown"
                    )
                    
                    await callback.message.answer(
                        "Введите номер услуги (например: 1):\n\n"
                        "Или нажмите Назад для отмены",
                        reply_markup=get_cancel_keyboard()
                    )
                    await state.update_data(services=services)
                    await state.set_state(BookingState.service)
                else:
                    await callback.message.edit_text(
                        " Не удалось загрузить услуги",
                        reply_markup=get_back_keyboard()
                    )
    except Exception as e:
        await callback.message.edit_text(
            f"Ошибка: {str(e)}",
            reply_markup=get_back_keyboard()
        )
    
    await callback.answer()

@router.message(BookingState.service)
async def process_service(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Запись отменена", reply_markup=get_back_keyboard())
        return
    
    try:
        service_number = int(message.text) - 1
        data = await state.get_data()
        services = data.get('services', [])
        
        if 0 <= service_number < len(services):
            service = services[service_number]
            await state.update_data(selected_service=service)
            
            await message.answer(
                f"Вы выбрали: {service['name']}\n"
                f"Цена: {service['price']}₽\n"
                f"Длительность: {service['duration']} мин\n\n"
                f"Введите дату и время в формате:\n"
                f"ДД.ММ.ГГГГ ЧЧ:ММ\n"
                f"Например: 15.01.2025 14:30",
                reply_markup=get_cancel_keyboard()
            )
            await state.set_state(BookingState.date)
        else:
            await message.answer("Неверный номер. Попробуйте ещё раз:")
    except ValueError:
        await message.answer("Введите число от 1 до 10!")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@router.message(BookingState.date)
async def process_date(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Запись отменена", reply_markup=get_back_keyboard())
        return
    
    try:
        date_text = message.text
        appointment_date = datetime.strptime(date_text, "%d.%m.%Y %H:%M")
        
        if appointment_date < datetime.now():
            await message.answer(
                "Нельзя записаться на прошедшее время.\n"
                "Введите дату и время в будущем:"
            )
            return
        
        await state.update_data(appointment_date=appointment_date.isoformat())
        
        await message.answer(
            "Введите ваше имя:",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(BookingState.name)
    except ValueError:
        await message.answer(
            "Неверный формат даты.\n"
            "Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Например: 15.01.2025 14:30"
        )

@router.message(BookingState.name)
async def process_name(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Запись отменена", reply_markup=get_back_keyboard())
        return
    
    if len(message.text.strip()) < 2:
        await message.answer("Имя слишком короткое. Введите полное имя:")
        return
    
    await state.update_data(client_name=message.text.strip())
    
    await message.answer(
        "Введите ваш телефон:\n"
        "Например: +7 (999) 123-45-67",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(BookingState.phone)

@router.message(BookingState.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Запись отменена", reply_markup=get_back_keyboard())
        return
    
    data = await state.get_data()
    service = data.get('selected_service')
    appointment_date = data.get('appointment_date')
    client_name = data.get('client_name')
    client_phone = message.text.strip()
    
    try:
        booking_data = {
            "service_id": service['id'],
            "master_id": None,
            "master_name": "Любой свободный мастер",
            "appointment_date": appointment_date,
            "client_name": client_name,
            "client_phone": client_phone,
            "comment": "Запись через Telegram бота",
            "status": "pending"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.API_URL}/bookings/",
                json=booking_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    await message.answer(
                        f"Запись создана!\n\n"
                        f"Услуга: {service['name']}\n"
                        f"Дата: {appointment_date[:16].replace('T', ' ')}\n"
                        f"Имя: {client_name}\n"
                        f"Телефон: {client_phone}\n"
                        f"Цена: {service['price']}₽\n\n"
                        f"Ждём вас в нашем салоне!\n"
                        f"г. Москва, ул. Примерная, 10",
                        parse_mode="Markdown"
                    )
                else:
                    error_detail = await response.json()
                    await message.answer(
                        f"Не удалось создать запись: {error_detail.get('detail', 'Неизвестная ошибка')}\n"
                        f"Попробуйте позже или свяжитесь с нами по телефону."
                    )
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
    finally:
        await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Запись отменена",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()