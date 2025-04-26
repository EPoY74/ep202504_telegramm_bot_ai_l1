"""
Основной файл телеграмм бота
Автор: Евгений Петров
Почта: p174@mail.ru
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

class Bot_Config:
    """
    Загружает конфигурацию Телеграмм бота
    """
    def __init__(self):
        load_dotenv()
        try:
            self.BOT_TOKEN: str|None = str(os.getenv("BOT_TOKEN"))
        except ValueError as err:
            logging.critical(f"Отсутствует BOT_TOKEN в .env файле: {err}")
            raise ValueError("Токен телеграм бота не найден") from err
        bot_admins: str|None = os.getenv("ADMINS_ID")
        if bot_admins:
            try:
                self.ADMINS_ID = [int(bot_admin_id.strip())
                                   for bot_admin_id in bot_admins.split(",")
                ]
            except ValueError as err:
                err_msg = (
                    "Ошибка в формате ID админимстратора(ов)"
                    f"(в т.ч. в .env - файле): {err}"
                )
                logging.error(err_msg)
                self.ADMINS_ID = []
                raise ValueError(err_msg) from err   



bot = Bot(token=str(os.getenv("BOT_TOKEN")))
dp = Dispatcher()


async def main():
    """
    Оcновная функция для запуска    
    """
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    """
    Запуск кода в асинхронном виде
    """

    logging.info("Запуск телеграм бота")
    asyncio.run(main())
