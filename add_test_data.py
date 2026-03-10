from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Service

print("🔄 Создание таблиц и добавление тестовых данных...")

# Создаём таблицы (на всякий случай)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Проверяем, есть ли данные
    existing = db.query(Service).count()
    if existing > 0:
        print("⚠️ Данные уже существуют!")
        db.close()
        exit()
    
    print("➕ Добавление услуг...")
    
    # Услуги
    services = [
        Service(
            name="Наращивание ногтей",
            description="Наращивание ногтей гелем или акрилом.",
            price=1000.00,
            duration=120,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Снятие покрытия",
            description="Бережное снятие старого покрытия.",
            price=500.00,
            duration=15,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Покрытие гель-лак",
            description="Покрытие гель-лаком любого цвета.",
            price=800.00,
            duration=60,
            category="Маникюр",
            is_active=True
        ),
    ]
    
    db.add_all(services)
    db.commit()
    
    print("✅ Тестовые данные добавлены!")
    print(f"Услуг: {len(services)}")
    
    for service in services:
        print(f"  - {service.name}: {service.price} руб.")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    db.rollback()
    
finally:
    db.close()
    print("🔌 Подключение закрыто.")