const API_URL = 'http://127.0.0.1:8000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const servicesList = document.getElementById('servicesList');
    const serviceSelect = document.getElementById('service');
    if (serviceSelect) {
        try {
            const response = await fetch(`${API_URL}/services/`);
            const services = await response.json();
            
            serviceSelect.innerHTML = services.map(service => 
                `<option value="${service.id}">${service.name} - ${service.price}₽</option>`
            ).join('');
        } catch (error) {
            console.error('Ошибка загрузки услуг:', error);
        }
    }

    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const bookingData = {
                service_id: parseInt(document.getElementById('service').value),
                client_name: document.getElementById('clientName').value,
                client_phone: document.getElementById('clientPhone').value,
                appointment_date: document.getElementById('appointmentDate').value,
                comment: document.getElementById('comment').value,
                status: 'pending'
            };
            try {
                const response = await fetch(`${API_URL}/bookings/`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(bookingData)
                });
                
            } catch (error) {
                alert('Ошибка: ' + error.message);
            }
        });
    }
});