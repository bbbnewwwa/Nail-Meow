from app.database import engine, Base

print("Создание таблиц в PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("Таблицы успешно созданы!")