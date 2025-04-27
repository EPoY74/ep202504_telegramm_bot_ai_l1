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


class EnvLoadError(Exception):
    """
    Класс для пробрасывания исключений
    """
    pass


class Bot_Config:
    """
    Загружает конфигурацию Телеграмм бота
    """
    def __init__(self) -> None:
        if not load_dotenv():
            err_msg = ".env не загружен или не найден"
            logging.warning(err_msg)
            raise EnvLoadError(err_msg)

        try:
            self.BOT_TOKEN: str = str(os.getenv("BOT_TOKEN"))
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


async def shutdown(dp: Dispatcher, bot: Bot):
    """
    Завершение телеграмм бота
    """

    logging.warning("Завершение работы телеграмм бота")
    
    try:
        await dp.storage.close()
    except Exception as err:
        err_msg=f"Ошибка закрытия storage: {err}"
        logging.error(err_msg)
        raise Exception(err_msg) from Exception

    try:
        await bot.session.close()
    except Exception as err:
        err_msg = f"Ошибка закрытия сессии: {err}"
        logging.error(err_msg)
        raise Exception(err_msg) from Exception

async def main():
    """
    Оcновная функция для запуска    
    """
    config = Bot_Config()
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    try:
        logging.info("Запуск телеграм бота")
        await dp.start_polling(bot)
    except Exception as err:
        err_msg = f"Ошибка при запуске бота: {err}"
        logging.error(err_msg)
        raise Exception(err_msg) from Exception
    finally:
        await shutdown(dp, bot)


if __name__ == "__main__":
    """
    Запуск кода в асинхронном виде
    """

    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit) as err:
        logging.info(f"Бот остановлен вручную: {err}")
    except Exception as err:
        err_msg = f"Критическая ошибка: {err}"
        logging.critical(err_msg)
        raise Exception(err_msg) from Exception

