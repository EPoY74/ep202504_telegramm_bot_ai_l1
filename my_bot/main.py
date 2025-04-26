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
load_dotenv()
bot = Bot(token=str(os.getenv("BOT_TOKEN")))
dp = Dispatcher()


async def main():
    """
    Оcновная функция для запуска    
    """
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    """
    Запуск кода в асинхронном dиде
    """

    logging.info("Запуск телеграм бота")
    asyncio.run(main())
