const API_URL = 'http://127.0.0.1:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Админ-панель загружена');
    loadStats();
    loadServicesList();
    loadServicesForEdit();
});

// ========== СТАТИСТИКА ==========
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/admin/stats`);
        const stats = await response.json();
        document.getElementById('servicesCount').textContent = stats.services || 0;
        document.getElementById('bookingsCount').textContent = stats.bookings || 0;
        document.getElementById('usersCount').textContent = stats.users || 0;
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
    }
}

// ========== СПИСОК УСЛУГ ==========
async function loadServicesList() {
    try {
        const response = await fetch(`${API_URL}/services/`);
        const services = await response.json();
        const container = document.getElementById('servicesAdmin');
        
        if (!container) return;
        
        if (services.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Услуг пока нет. Добавьте первую услугу!</p>';
            return;
        }
        
        container.innerHTML = services.map(service => `
            <div class="admin-card">
                <h3>${escapeHtml(service.name)}</h3>
                <div class="price">${service.price} ₽</div>
                <p>⏱ ${service.duration || 60} мин</p>
                <p>📁 ${escapeHtml(service.category || 'Общее')}</p>
                <div class="admin-actions">
                    <button onclick="quickEditPrice(${service.id}, ${service.price})" class="btn-edit">✏️ Цена</button>
                    <button onclick="deleteService(${service.id})" class="btn-delete">🗑️</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        const container = document.getElementById('servicesAdmin');
        if (container) container.innerHTML = '<p class="error">Не удалось загрузить услуги.</p>';
    }
}

// ========== БЫСТРОЕ ИЗМЕНЕНИЕ ЦЕНЫ ==========
async function quickEditPrice(id, currentPrice) {
    const newPrice = prompt(`Новая цена:`, currentPrice);
    if (newPrice && !isNaN(newPrice)) {
        try {
            const response = await fetch(`${API_URL}/services/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ price: parseFloat(newPrice) })
            });
            if (response.ok) {
                alert('✅ Цена обновлена!');
                loadServicesList();
                loadStats();
                loadServicesForEdit();
            } else {
                alert('❌ Ошибка при обновлении');
            }
        } catch (error) {
            alert('Ошибка: ' + error.message);
        }
    }
}

// ========== УДАЛЕНИЕ УСЛУГИ ==========
async function deleteService(id) {
    if (confirm('Удалить услугу?')) {
        try {
            const response = await fetch(`${API_URL}/services/${id}`, { method: 'DELETE' });
            if (response.ok) {
                alert('✅ Услуга удалена!');
                loadServicesList();
                loadStats();
                loadServicesForEdit();
            } else {
                alert('❌ Ошибка при удалении');
            }
        } catch (error) {
            alert('Ошибка: ' + error.message);
        }
    }
}

// ========== ЗАГРУЗКА СПИСКА ДЛЯ РЕДАКТИРОВАНИЯ ==========
async function loadServicesForEdit() {
    try {
        const response = await fetch(`${API_URL}/services/`);
        const services = await response.json();
        const select = document.getElementById('editServiceSelect');
        if (!select) return;
        
        select.innerHTML = '<option value="">-- Выберите услугу --</option>';
        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = `${service.name} - ${service.price} ₽`;
            select.appendChild(option);
        });
        
        select.onchange = function() {
            const selectedService = services.find(s => s.id == this.value);
            if (selectedService) {
                showEditForm(selectedService);
            } else {
                hideEditForm();
            }
        };
    } catch (error) {
        console.error('Ошибка загрузки услуг:', error);
    }
}

// ========== ПОКАЗАТЬ/СКРЫТЬ ФОРМУ РЕДАКТИРОВАНИЯ ==========
function showEditForm(service) {
    const form = document.getElementById('editServiceForm');
    if (!form) return;
    
    document.getElementById('editServiceId').value = service.id;
    document.getElementById('editServiceName').value = service.name;
    document.getElementById('editServicePrice').value = service.price;
    document.getElementById('editServiceDuration').value = service.duration || '';
    document.getElementById('editServiceCategory').value = service.category || '';
    document.getElementById('editServiceDescription').value = service.description || '';
    
    form.style.display = 'grid';
}

function hideEditForm() {
    const form = document.getElementById('editServiceForm');
    if (form) {
        form.style.display = 'none';
        const select = document.getElementById('editServiceSelect');
        if (select) select.value = '';
    }
}

function cancelEdit() {
    hideEditForm();
}

// ========== ОБНОВЛЕНИЕ УСЛУГИ ==========
async function updateService() {
    const serviceId = document.getElementById('editServiceId').value;
    if (!serviceId) {
        alert('❌ Выберите услугу для редактирования');
        return;
    }
    
    const updatedData = {
        name: document.getElementById('editServiceName').value.trim(),
        price: parseFloat(document.getElementById('editServicePrice').value),
        duration: parseInt(document.getElementById('editServiceDuration').value) || 60,
        category: document.getElementById('editServiceCategory').value.trim() || 'Общее',
        description: document.getElementById('editServiceDescription').value.trim()
    };
    
    if (!updatedData.name || !updatedData.price) {
        alert('❌ Название и цена обязательны!');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/services/${serviceId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        });
        
        if (response.ok) {
            alert('✅ Услуга обновлена!');
            hideEditForm();
            loadStats();
            loadServicesList();
            loadServicesForEdit();
        } else {
            alert('❌ Ошибка при обновлении');
        }
    } catch (error) {
        alert('Ошибка: ' + error.message);
    }
}

// ========== ДОБАВЛЕНИЕ УСЛУГИ ==========
const addServiceForm = document.getElementById('addServiceForm');
if (addServiceForm) {
    addServiceForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const newService = {
            name: document.getElementById('serviceName').value.trim(),
            price: parseFloat(document.getElementById('servicePrice').value),
            duration: parseInt(document.getElementById('serviceDuration').value) || 60,
            category: document.getElementById('serviceCategory').value.trim() || 'Общее',
            description: document.getElementById('serviceDescription').value.trim(),
            is_active: true
        };
        
        if (!newService.name || !newService.price) {
            alert('❌ Название и цена обязательны!');
            return;
        }
        
        try {
            const response = await fetch(`${API_URL}/services/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newService)
            });
            
            if (response.ok) {
                alert('✅ Услуга добавлена!');
                addServiceForm.reset();
                loadStats();
                loadServicesList();
                loadServicesForEdit();
            } else {
                alert('❌ Ошибка при добавлении');
            }
        } catch (error) {
            alert('Ошибка: ' + error.message);
        }
    });
}

// ========== ЗАЩИТА ОТ XSS ==========
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}