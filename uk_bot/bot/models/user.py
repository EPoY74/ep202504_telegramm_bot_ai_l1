"""
Модель пользователя
"""

from bot.db import Base
from sqlalchemy import BigInteger, Column, String


class User(Base):
    __tablenname__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
