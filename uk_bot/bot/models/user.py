"""
Модель пользователя
"""

from bot.db import Base
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablenname__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
