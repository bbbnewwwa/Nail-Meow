from sqlalchemy import create_engine, inspect, text
from app.config import settings

print("🔍 Проверка базы данных PostgreSQL...")
print(f"📁 Подключение: {settings.DATABASE_URL}")
print()

try:
    # Создаем движок
    engine = create_engine(settings.DATABASE_URL)
    
    # Проверяем подключение
    with engine.connect() as connection:
        print("✅ Подключение к базе данных успешно!")
        print()
        
        # Получаем список всех таблиц
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"📋 Найдено таблиц: {len(tables)}")
            print()
            
            for table_name in tables:
                print(f"📊 Таблица: {table_name}")
                print("-" * 50)
                
                # Получаем информацию о колонках
                columns = inspector.get_columns(table_name)
                print(f"  Колонки ({len(columns)}):")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    print(f"    - {col['name']}: {col['type']} {nullable}")
                
                # Получаем информацию о первичных ключах
                pk_constraint = inspector.get_pk_constraint(table_name)
                if pk_constraint['constrained_columns']:
                    print(f"  Первичный ключ: {', '.join(pk_constraint['constrained_columns'])}")
                
                # Получаем информацию о внешних ключах
                fk_constraints = inspector.get_foreign_keys(table_name)
                if fk_constraints:
                    print(f"  Внешние ключи:")
                    for fk in fk_constraints:
                        print(f"    - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
                
                print()
        else:
            print("⚠️ В базе данных НЕТ таблиц!")
            print()
            print("💡 Запустите для создания таблиц:")
            print("   python create_tables.py")
        
        # Считаем количество записей в каждой таблице
        print("📈 Количество записей:")
        for table_name in tables:
            try:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                print(f"  {table_name}: {count} записей")
            except Exception as e:
                print(f"  {table_name}: ошибка при подсчете - {e}")
        
        print()
        print("✅ Проверка завершена!")

except Exception as e:
    print(f"❌ Ошибка подключения к базе данных:")
   