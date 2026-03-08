from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Service, ServiceCategory, Master

# Создаём все таблицы
Base.metadata.create_all(bind=engine)

# Создаём сессию
db = SessionLocal()

try:
    # Проверяем, есть ли уже данные
    existing_categories = db.query(ServiceCategory).count()
    if existing_categories > 0:
        print("Данные уже существуют в базе!")
        db.close()
        exit()
    
    # Добавляем категории
    cat1 = ServiceCategory(name="Маникюр", description="Услуги по маникюру")
    cat2 = ServiceCategory(name="Педикюр", description="Услуги по педикюру")
    cat3 = ServiceCategory(name="Дизайн ногтей", description="Дизайн и декор")
    
    db.add_all([cat1, cat2, cat3])
    db.commit()
    
    # Добавляем услуги
    services = [
        Service(name="Маникюр классический", category_id=cat1.id, price=500.00, duration=30, description="Обычный маникюр без покрытия"),
        Service(name="Покрытие гель-лак", category_id=cat1.id, price=1200.00, duration=60, description="Маникюр + покрытие гель-лак"),
        Service(name="Маникюр комбинированный", category_id=cat1.id, price=800.00, duration=45, description="Аппаратный + ножничный маникюр"),
        Service(name="Наращивание ногтей", category_id=cat1.id, price=2000.00, duration=120, description="Наращивание акрилом или гелем"),
        Service(name="Снятие покрытия", category_id=cat1.id, price=300.00, duration=15, description="Снятие гель-лака"),
        Service(name="Педикюр полный", category_id=cat2.id, price=1500.00, duration=90, description="Полный педикюр с покрытием"),
        Service(name="SPA педикюр", category_id=cat2.id, price=1800.00, duration=120, description="Педикюр с SPA уходом"),
        Service(name="Педикюр экспресс", category_id=cat2.id, price=900.00, duration=45, description="Быстрый педикюр без покрытия"),
        Service(name="Дизайн стразы", category_id=cat3.id, price=300.00, duration=15, description="Дизайн стразами (1 ноготь)"),
        Service(name="Френч", category_id=cat3.id, price=500.00, duration=30, description="Французский маникюр"),
        Service(name="Омбре", category_id=cat3.id, price=600.00, duration=40, description="Градиентный дизайн"),
        Service(name="Роспись", category_id=cat3.id, price=800.00, duration=60, description="Художественная роспись"),
    ]
    
    db.add_all(services)
    db.commit()
    
    # Добавляем мастеров
    masters = [
        Master(full_name="Иванова Мария", specialization="Мастер маникюра", rating=4.9, description="Опыт работы 5 лет"),
        Master(full_name="Петрова Анна", specialization="Мастер педикюра", rating=4.8, description="Опыт работы 3 года"),
        Master(full_name="Сидорова Елена", specialization="Дизайнер ногтей", rating=5.0, description="Опыт работы 7 лет"),
    ]
    
    db.add_all(masters)
    db.commit()
    
    print("Тестовые данные успешно добавлены!")
    print(f"Создано категорий: 3")
    print(f"Создано услуг: {len(services)}")
    print(f"Создано мастеров: {len(masters)}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    db.rollback()
finally:
    db.close()