from app.database import engine, Base
from app import models

print("🔄 Создание таблиц в PostgreSQL...")

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

print("✅ Таблицы успешно созданы!")

# Проверяем, что таблицы действительно созданы
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"\n📋 Создано таблиц: {len(tables)}")
for table in tables:
    print(f"  - {table}")

print("\n✨ Готово! Теперь можно добавить тестовые данные:")
print("   python add_test_data.py")