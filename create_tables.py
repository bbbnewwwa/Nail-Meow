from app.database import engine, Base

# Создаём все таблицы
Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы!")
print("База данных: nailmeow.db")