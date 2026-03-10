from app.database import engine
from sqlalchemy import text

print(" Проверяю подключение...")

try:
    with engine.connect() as conn:
        # Проверяем, к какой базе подключились
        result = conn.execute(text("SELECT current_database()"))
        db_name = result.fetchone()[0]
        print(f" База данных: {db_name}")
        
        # Проверяем таблицы
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = result.fetchall()
        
        if tables:
            print(f"Найдено таблиц: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("Таблиц нет в базе!")
            
except Exception as e:
    print(f" Ошибка подключения: {e}")