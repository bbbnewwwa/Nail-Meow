const API_URL = 'http://127.0.0.1:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Страница загружена, загружаем услуги...');
    
    // Загрузка услуг
    loadServices();
    
    // Обработка формы
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        console.log('✅ Форма найдена, добавляем обработчик...');
        
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // ← ОЧЕНЬ ВАЖНО!
            
            console.log('📝 Отправка формы...');
            
            const formData = {
                client_name: document.getElementById('clientName').value,
                client_phone: document.getElementById('clientPhone').value,
                service_id: parseInt(document.getElementById('service').value),
                appointment_date: document.getElementById('appointmentDate').value,
                comment: document.getElementById('comment').value || "",
                status: 'pending'
            };
            
            console.log('Данные для отправки:', formData);
            
            try {
                const response = await fetch(`${API_URL}/bookings/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                console.log('Статус ответа:', response.status);
                
                if (response.ok) {
                    const result = await response.json();
                    console.log('✅ Запись создана:', result);
                    alert('✅ Запись успешно создана! Мы свяжемся с вами для подтверждения.');
                    bookingForm.reset();
                } else {
                    const error = await response.json();
                    console.error('❌ Ошибка сервера:', error);
                    alert('❌ Ошибка при создании записи: ' + JSON.stringify(error));
                }
            } catch (error) {
                console.error('❌ Ошибка сети:', error);
                alert('❌ Ошибка: ' + error.message);
            }
        });
    } else {
        console.error('❌ Форма не найдена!');
    }
});

async function loadServices() {
    try {
        console.log('🔄 Загрузка услуг...');
        const response = await fetch(`${API_URL}/services/`);
        const services = await response.json();
        
        console.log('✅ Услуги загружены:', services);
        
        const serviceSelect = document.getElementById('service');
        if (serviceSelect) {
            serviceSelect.innerHTML = '<option value="">Выберите услугу</option>' +
                services.map(service => 
                    `<option value="${service.id}">${service.name} - ${service.price} ₽</option>`
                ).join('');
        }
    } catch (error) {
        console.error('❌ Ошибка загрузки услуг:', error);
    }
}