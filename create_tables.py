from app.database import engine, Base
from app import models

print("🔄 Создание таблиц в PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Таблицы успешно созданы!")

# Показать какие таблицы созданы
print("\n📋 Загруженные модели:")
print(f"  - Service: {models.Service}")
print(f"  - User: {models.User}")
print(f"  - Booking: {models.Booking}")
print("\n✨ Готово! Теперь можно добавить тестовые данные:")
print("   python add_test_data.py")