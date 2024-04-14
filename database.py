import sqlite3
import logging
from system_config import DB_NAME


def create_table(db_name=DB_NAME):
    try:
        # Создаём подключение к базе данных
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Создаём таблицу
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                tts_symbols INTEGER)
            ''')
            # Сохраняем изменения
            conn.commit()
            logging.info("База данных успешно создана")  # Выводим сообщение в лог о том, что база данных создана
    except Exception as e:
        logging.debug(f"Error: {e}")


def process_query(query, params, db_name="DB_NAME"):
    connection = sqlite3.connect(db_name)  # Устанавливаем соединение с базой данных
    connection.row_factory = sqlite3.Row  # Устанавливаем формат возвращаемых данных
    cur = connection.cursor()
    if not params:
        if 'SELECT' in query:
            result = cur.execute(query)
            return result
        cur.execute(query)
    else:
        if 'SELECT' in query:
            result = cur.execute(query, tuple(params))
            return list(result)
        cur.execute(query, tuple(params))
    connection.commit()  # Сохраняем изменения в базе данных
    connection.close()  # Закрываем соединение


def insert_row(user_id, message, tts_symbols, db_name="DB_NAME"):
    try:
        # Подключаемся к базе
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Вставляем в таблицу новое сообщение
            cursor.execute('''INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)''',
                           (user_id, message, tts_symbols))
            # Сохраняем изменения
            conn.commit()
    except Exception as e:  # обрабатываем ошибку и записываем её в переменную <e>
        logging.debug(f"Error: {e}")


def count_all_symbol(user_id, db_name=DB_NAME):
    try:
        # Подключаемся к базе
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Считаем, сколько символов использовал пользователь
            cursor.execute('''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            # Проверяем data на наличие хоть какого-то полученного результата запроса
            # И на то, что в результате запроса мы получили какое-то число в data[0]
            if data and data[0]:
                # Если результат есть и data[0] == какому-то числу, то
                return data[0]  # возвращаем это число - сумму всех потраченных символов
            else:
                # Результата нет, так как у нас ещё нет записей о потраченных символах
                return 0  # возвращаем 0
    except Exception as e:
        logging.debug(f"Error: {e}")
