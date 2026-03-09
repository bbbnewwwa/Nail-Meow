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
});