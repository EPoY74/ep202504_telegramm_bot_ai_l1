"""
Работа с БД
"""

import logging
import sqlite3

import aiosqlite

DB_NAME: str = "user.db"


async def init_db() -> None:
    """
    Инициализирую БД для работы
    """

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                user_email TEXT         
            )
        """)
        await db.commit()


async def user_append(user_id: int, user_name: str, user_email: str) -> None:
    """
    Добавляет пользователя в базу данных

    :param user_id: ИД пользователя в телеграм
    :type user_id: int
    :param user_name: Имя пользователя в телеграм
    :type user_name: str
    :param user_email: Электронная почта пользователя
    :type user_email: str
    """
    # if aiosqlite.connect(DB_NAME) is not None:
    #     logging.warning("Создаю БД")
    #     await init_db()

    DB_NAME_RW = (
        "file:" + DB_NAME + "?mode=rw"
    )  # Открываем БД на Read-Write. Создавать - не будем.
    
    try:
        async with aiosqlite.connect(DB_NAME_RW) as db_connect:
            
            sql_query: str = """INSERT 
                    INTO users (user_id, user_name, user_email) 
                    VALUES (?, ?, ?)"""
            await db_connect.execute(sql_query, (user_id, user_name, user_email))
            await db_connect.com    mit()
    except sqlite3.OperationalError as err:
        logging.warning("Не могу открыть файл БД!")
        logging.error(f"Ошибка: {err}")
        await init_db()

