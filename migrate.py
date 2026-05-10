# Создайте временный скрипт migrate_orders.py
from back.data import db_session
from sqlalchemy import text

db_session.global_init('db.sqlite')
session = db_session.create_session()

try:
    # Добавляем колонку user_id
    session.execute(text('ALTER TABLE orders ADD COLUMN user_id INTEGER REFERENCES users(id)'))
    session.commit()
    print("Колонка user_id успешно добавлена")
except Exception as e:
    print(f"Ошибка: {e}. Возможно колонка уже существует.")
    session.rollback()