from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Service, User

# Создаём таблицы
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Проверяем, есть ли данные
    existing = db.query(Service).count()
    if existing > 0:
        print("⚠️ Данные уже существуют!")
        db.close()
        exit()
    
    # Услуги
    services = [
        Service(
            name="Наращивание ногтей",
            description="Наращивание ногтей гелем или акрилом. Идеальная форма и долговременный результат.",
            price=1000.00,
            duration=120,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Снятие покрытия",
            description="Бережное снятие старого покрытия без повреждения натуральной ногтевой пластины.",
            price=500.00,
            duration=15,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Покрытие гель-лак",
            description="Покрытие гель-лаком любого цвета. Стойкость до 3-х недель, блеск и красота!",
            price=800.00,
            duration=60,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Дизайн ногтей",
            description="Дизайн стразами, роспись, френч. Индивидуальный подход к каждому клиенту.",
            price=300.00,
            duration=30,
            category="Дизайн",
            is_active=True
        ),
        Service(
            name="SPA-уход",
            description="Комплексный уход за ногтями и кутикулой. Питание и увлажнение.",
            price=600.00,
            duration=45,
            category="Уход",
            is_active=True
        ),
    ]
    
    db.add_all(services)
    db.commit()
    
    print("✅ Тестовые данные добавлены!")
    print(f"Услуг: {len(services)}")
    print("\n📋 Добавленные услуги:")
    for service in services:
        print(f"  - {service.name}: {service.price} ₽ ({service.duration} мин)")