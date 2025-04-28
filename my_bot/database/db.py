"""
Работа с БД
"""

import aiosqlite

DB_NAME: str = "user.db"


async def init_db() -> None:
    """
    Инициализирую БД для работы
    """

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRYMARY KEY AUTOINCREMENT,
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

    async with aiosqlite.connect(DB_NAME) as db:
        sql_query: str = (
            "INSERT INTO users (user_id, user_name, user_email) VALUES ? ? ?"
        )
        await db.execute(sql_query, (user_id, user_name, user_email))
    await db.commit()