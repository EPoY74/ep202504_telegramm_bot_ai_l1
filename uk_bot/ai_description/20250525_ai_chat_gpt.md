Вот минимальный шаблон Telegram-бота на Python с использованием **Aiogram 3.x** и **PostgreSQL** через **SQLAlchemy**. Этот каркас можно расширять для реализации функционала, необходимого для управляющей компании (УК).

---

## 📁 Структура проекта

```
uk_bot/
├── bot/
│   ├── handlers/
│   │   └── start.py
│   ├── models/
│   │   └── user.py
│   ├── db.py
│   ├── config.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## 📦 Установка зависимостей

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

Установите необходимые библиотеки:

```bash
pip install aiogram sqlalchemy asyncpg python-dotenv
```

---

## ⚙️ Файл `.env`

Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:

```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/uk_bot_db
```

---

## 🛠️ `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

## 🗄️ `db.py` — настройка базы данных

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
```

---

## 👤 `models/user.py` — модель пользователя

```python
from sqlalchemy import Column, BigInteger, String
from bot.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
```

---

## 🚀 `handlers/start.py` — обработка команды /start

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.models.user import User
from bot.db import SessionLocal

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(
                id=message.from_user.id,
                full_name=message.from_user.full_name,
                phone=None
            )
            session.add(user)
            await session.commit()
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!")
```

---

## 🧠 `main.py` — запуск бота

```python
import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import start
from bot.db import engine, Base

async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ✅ Запуск бота

```bash
python bot/main.py
```

---

## 📌 Рекомендации по расширению

* **Миграции базы данных**: Используйте [Alembic](https://alembic.sqlalchemy.org/) для управления изменениями схемы базы данных.
* **Управление состояниями**: Реализуйте Finite State Machine (FSM) для пошагового взаимодействия с пользователем.
* **Административный интерфейс**: Добавьте веб-интерфейс для сотрудников УК с использованием фреймворков, таких как [FastAPI](https://fastapi.tiangolo.com/) или [Flask](https://flask.palletsprojects.com/).
* **Оповещения**: Реализуйте массовые рассылки уведомлений о плановых работах, собраниях и других событиях.

---

Если вам потребуется помощь в настройке окружения, создании миграций или реализации конкретных функций — обращайтесь!
