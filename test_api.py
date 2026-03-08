from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Service, Master, User, Product

# Создаём все таблицы
Base.metadata.create_all(bind=engine)

# Создаём сессию
db = SessionLocal()

try:
    # Проверяем, есть ли уже данные
    existing_services = db.query(Service).count()
    if existing_services > 0:
        print("Данные уже существуют в базе!")
        print(f"Найдено услуг: {existing_services}")
        db.close()
        exit()
    
    # Добавляем услуги (category — это просто строка!)
    services = [
        Service(
            name="Маникюр классический",
            description="Обычный маникюр без покрытия",
            price=500.00,
            duration=30,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Покрытие гель-лак",
            description="Маникюр + покрытие гель-лак",
            price=1200.00,
            duration=60,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Маникюр комбинированный",
            description="Аппаратный + ножничный маникюр",
            price=800.00,
            duration=45,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Наращивание ногтей",
            description="Наращивание акрилом или гелем",
            price=2000.00,
            duration=120,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Снятие покрытия",
            description="Снятие гель-лака",
            price=300.00,
            duration=15,
            category="Маникюр",
            is_active=True
        ),
        Service(
            name="Педикюр полный",
            description="Полный педикюр с покрытием",
            price=1500.00,
            duration=90,
            category="Педикюр",
            is_active=True
        ),
        Service(
            name="SPA педикюр",
            description="Педикюр с SPA уходом",
            price=1800.00,
            duration=120,
            category="Педикюр",
            is_active=True
        ),
        Service(
            name="Педикюр экспресс",
            description="Быстрый педикюр без покрытия",
            price=900.00,
            duration=45,
            category="Педикюр",
            is_active=True
        ),
        Service(
            name="Дизайн стразы",
            description="Дизайн стразами (1 ноготь)",
            price=300.00,
            duration=15,
            category="Дизайн",
            is_active=True
        ),
        Service(
            name="Френч",
            description="Французский маникюр",
            price=500.00,
            duration=30,
            category="Дизайн",
            is_active=True
        ),
    ]
    
    db.add_all(services)
    db.commit()
    
    # Добавляем мастеров
    masters = [
        Master(
            full_name="Иванова Мария",
            specialization="Мастер маникюра",
            rating=4.9,
            description="Опыт работы 5 лет",
            is_active=True
        ),
        Master(
            full_name="Петрова Анна",
            specialization="Мастер педикюра",
            rating=4.8,
            description="Опыт работы 3 года",
            is_active=True
        ),
        Master(
            full_name="Сидорова Елена",
            specialization="Дизайнер ногтей",
            rating=5.0,
            description="Опыт работы 7 лет",
            is_active=True
        ),
    ]
    
    db.add_all(masters)
    db.commit()
    
    print("Тестовые данные успешно добавлены!")
    print(f"Создано услуг: {len(services)}")
    print(f"Создано мастеров: {len(masters)}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    db.rollback()
finally:
    db.close()