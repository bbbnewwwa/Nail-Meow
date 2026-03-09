from app.database import engine, Base
from app import models
from sqlalchemy import inspect

print("Создание таблиц в PostgreSQL...")

# Проверяем, что модели загружены
print("Загруженные модели:")
print(f"   - Service: {models.Service}")
print(f"   - Master: {models.Master}")
print(f"   - User: {models.User}")
print(f"   - Booking: {models.Booking}")

# Создаём таблицы
Base.metadata.create_all(bind=engine)

print("Таблицы созданы!")

# Проверяем, что создалось
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f" Создано таблиц: {len(tables)}")
for table in tables:
    print(f"    {table}")