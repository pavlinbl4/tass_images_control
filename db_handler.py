import os
import sqlite3

base_path = os.path.join(os.path.dirname(__file__), 'sent_files.db')


def initialize_database():
    """
    Создает базу данных и таблицу, если они не существуют.
     """

    # conn = sqlite3.connect('sent_files.db')
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sent_files (image_id TEXT,
            image_caption TEXT,
            image_link TEXT,
            check_date TEXT)''')
    conn.commit()
    conn.close()




def log_file_sent(image_id, image_caption, image_link):
    """
    Логирует отправку файла в базу данных.
    """
    # conn = sqlite3.connect('sent_files.db')
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_files (image_id, image_caption, image_link, check_date) VALUES (?, ?, ?, datetime('now', '+3 hours'))",
                   (image_id, image_caption, image_link))
    conn.commit()
    conn.close()


def is_file_sent(image_id):
    """
    Проверяет, отправлялся ли файл ранее.
    """
    conn = sqlite3.connect('sent_files.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_files WHERE image_id = ?", (image_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def read_data_from_db(db_file, query):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Выполнение SQL-запроса
    cursor.execute(query)

    # Чтение всех строк результата запроса
    rows = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    return rows


if __name__ == '__main__':
    initialize_database()

    # log_file_sent('image_id_3', 'image_caption_2', 'image_link_2')

    _query = 'SELECT * FROM sent_files;'  # SQL-запрос для получения всех данных
    data = read_data_from_db(base_path, _query)
    for row in data:
        print(row)  # Выводим каждую строку результата
