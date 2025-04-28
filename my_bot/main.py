"""
Основной файл телеграмм бота
Автор: Евгений Петров
Почта: p174@mail.ru
@ep_20250446_edu_test_bot id=7891443548
# from builtins import ExceptionGroup
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.user import router as user_router

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
        """
        Docstring for __init__

        :param self: Description
        :type self:
        """
        if not load_dotenv():
            err_msg = ".env не загружен или не найден"
            logging.warning(err_msg)
            raise EnvLoadError(err_msg)

        try:
            self.BOT_TOKEN: str = str(os.getenv("BOT_TOKEN", default=None))
        except ValueError as err:
            logging.critical(f"Отсутствует BOT_TOKEN в .env файле: {err}")
            raise ValueError("Токен телеграм бота не найден") from err
        bot_admins: str | None = os.getenv("ADMINS_ID", default=None)
        if bot_admins:
            try:
                self.ADMINS_ID = [
                    int(bot_admin_id.strip())
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

    # @staticmethod
    # def load_config() -> Bot_Config | None:
    #     # ...


async def shutdown(dp: Dispatcher, bot: Bot) -> None:
    """
    Завершение телеграмм бота
    """

    logging.info("Завершение работы телеграмм бота")

    shutdown_results = await asyncio.gather(
        #  Закрываю асинхронно хранилище и сессию
        #  что бы корректно освободить ресурсы и обработать исключения
        dp.storage.close(),
        bot.session.close(),
        #  Что бы не падало при ошибках, устанавляваем True
        return_exceptions=True,
    )

    result_shutdown_errors: list = []
    for closed_item_status in shutdown_results:
        for closed_item_status in shutdown_results:
            if isinstance(closed_item_status, Exception):
                logging.error(f"Ошибка при закрытии: {closed_item_status}")
                result_shutdown_errors.append(closed_item_status)
        if len(result_shutdown_errors) > 0:
            raise ExceptionGroup(
                "Ошибки при закрытии бота", result_shutdown_errors
            )
    if not result_shutdown_errors:
        logging.info("Телеграм бот завершил работу корректно.")


async def main() -> None:
    """
    Оcновная функция для запуска телеграм бота
    """
    config = Bot_Config()
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)

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
    Запуск скрипта в асинхронном виде
    """
    asyncio.run(main())
