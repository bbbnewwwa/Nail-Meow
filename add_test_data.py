from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Service, Master

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    services = [
        Service(name="Маникюр классический", description="Обычный маникюр", price=500.00, duration=30, category="Маникюр", is_active=True),
        Service(name="Покрытие гель-лак", description="Гель-лак", price=1200.00, duration=60, category="Маникюр", is_active=True),
        Service(name="Наращивание ногтей", description="Наращивание", price=2000.00, duration=120, category="Маникюр", is_active=True),
        Service(name="Педикюр полный", description="Полный педикюр", price=1500.00, duration=90, category="Педикюр", is_active=True),
        Service(name="SPA педикюр", description="SPA уход", price=1800.00, duration=120, category="Педикюр", is_active=True),
    ]
    
    db.add_all(services)
    db.commit()
    
    masters = [
        Master(full_name="Иванова Мария", specialization="Мастер маникюра", rating=4.9, description="Опыт 5 лет", is_active=True),
        Master(full_name="Петрова Анна", specialization="Мастер педикюра", rating=4.8, description="Опыт 3 года", is_active=True),
    ]
    
    db.add_all(masters)
    db.commit()
    
    print("✅ Данные добавлены!")
except Exception as e:
    print(f"Ошибка: {e}")
    db.rollback()
finally:
    db.close()