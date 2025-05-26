"""
Загружает конфигурацию из переменных окружения
"""

import logging
import os

import dotenv


class EnvLoadError(Exception):
    """
    Класс для пробрасывания исключений
    """

    pass


def logger_init() -> None:
    """
    Инициализирую логгер в требуемом мне формате
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )


def check_env_var_ok(var_config: str | None, var_name: str) -> str:
    """
    Проверяет существование переменной
    """
    if not var_config:
        err_msg = f"Переменная окружения {var_name} не задана"
        logging.error(err_msg)
        raise EnvLoadError(err_msg)
    else:
        return var_config


def load_bot_env() -> dict[str, str]:
    """
    Загружает конфиденциальные данные из переменных окружения
    """
    logger_init()
    if not dotenv.load_dotenv():
        err_msg = "Ошибка загрузки файла с переменными окружения .env"
        logging.error(err_msg)
        raise (EnvLoadError(err_msg))

    telegram_bot_token = os.getenv("BOT_TOKEN")
    db_connect_url = os.getenv("DATABASE_URL")

    telegram_bot_token = check_env_var_ok(telegram_bot_token, "BOT_TOKEN")
    db_connect_url = check_env_var_ok(db_connect_url, "DATABASE_URL")

    bot_config = {
        "BOT_TOKEN": telegram_bot_token,
        "DATABASE_URL": db_connect_url,
    }

    return bot_config
