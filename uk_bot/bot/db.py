"""
Работа с базой данных
Автор: ЕВгений Петров
Почта: epoy74@gmail.com
"""

from typing import Any

from config import load_bot_env
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


def load_uk_bot_configuration() -> dict[str, str]:
    """
    Загружает конфигурацию чатбота для подключения к БД
    """
    uk_bot_settings = load_bot_env()
    return uk_bot_settings

class Base(DeclarativeBase):
    """
    Базовый класс для модулей
    """    
    pass


def create_async_session() -> async_sessionmaker[AsyncSession]:
    """
    Создает асинхронный движок и фабрику сессий для работы с базой данных.
    """
    uk_telegram_bot_settings = load_uk_bot_configuration()
    engine = create_async_engine(
        uk_telegram_bot_settings["DATABASE_URL"], echo=True
    )
    SessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return SessionLocal
