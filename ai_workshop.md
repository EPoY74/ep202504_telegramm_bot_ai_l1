Отлично! Начнем с **воркшопа по Aiogram 3.x**, где создадим бота с регистрацией, профилем и простой админкой. Это база для 90% коммерческих ботов.  

---

## **🎯 Воркшоп #1: Бот на Aiogram с FSM и SQLite**  
**Цель:** Бот, который умеет:  
✅ Регистрировать пользователя (имя, email)  
✅ Хранить данные в SQLite  
✅ Показывать профиль по команде `/profile`  
✅ Иметь админ-панель для просмотра всех юзеров  

---

### **🛠 Технологии:**  
- Python 3.10+  
- Aiogram 3.x (асинхронная библиотека)  
- SQLite (позже переедем на PostgreSQL)  
- FSM (Finite State Machine) для многошаговых форм  

---

### **📌 Шаг 1: Установка и настройка**  
1. Создаем виртуальное окружение:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

2. Устанавливаем зависимости:  
   ```bash
   pip install aiogram python-dotenv
   ```

3. Создаем структуру проекта:  
   ```
   my_bot/
   ├── .env           # Токен бота
   ├── main.py        # Главный файл
   ├── handlers/      # Обработчики команд
   │   ├── __init__.py
   │   ├── user.py    # Команды юзеров
   │   └── admin.py   # Админ-команды
   └── database/      # Работа с БД
       ├── __init__.py
       └── db.py      # SQLite-запросы
   ```

---

### **📌 Шаг 2: Токен бота и запуск**  
1. Получи токен у [@BotFather](https://t.me/BotFather).  
2. Создай `.env` файл:  
   ```ini
   BOT_TOKEN=ваш_токен
   ADMIN_ID=ваш_телеграм_id  # Чтобы получать админ-сообщения
   ```
3. Напишем минимальный `main.py`:  
   ```python
   import logging
   from aiogram import Bot, Dispatcher
   from dotenv import load_dotenv
   import os

   load_dotenv()

   bot = Bot(token=os.getenv("BOT_TOKEN"))
   dp = Dispatcher()

   async def main():
       logging.basicConfig(level=logging.INFO)
       await dp.start_polling(bot)

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())
   ```
   Запусти:  
   ```bash
   python main.py
   ```
   Бот должен включиться без ошибок.  

---

### **📌 Шаг 3: Регистрация пользователя через FSM**  
1. В `handlers/user.py` добавляем:  
   ```python
   from aiogram import F, Router
   from aiogram.fsm.context import FSMContext
   from aiogram.types import Message

   router = Router()

   @router.message(F.text == "/start")
   async def cmd_start(message: Message, state: FSMContext):
       await message.answer("Привет! Как тебя зовут?")
       await state.set_state("waiting_name")  # Устанавливаем состояние

   @router.message(F.state == "waiting_name")
   async def process_name(message: Message, state: FSMContext):
       await state.update_data(name=message.text)  # Сохраняем имя
       await message.answer("Отправь свой email:")
       await state.set_state("waiting_email")  # Меняем состояние

   @router.message(F.state == "waiting_email")
   async def process_email(message: Message, state: FSMContext):
       data = await state.get_data()  # Достаем имя
       await message.answer(
           f"Регистрация завершена!\n"
           f"Имя: {data['name']}\n"
           f"Email: {message.text}"
       )
       await state.clear()  # Чистим состояние
   ```
2. Подключаем роутер в `main.py`:  
   ```python
   from handlers.user import router as user_router
   dp.include_router(user_router)
   ```

**Проверяем:**  
- Отправляем `/start` → имя → email.  
- Бот должен вывести итоговые данные.  

---

### **📌 Шаг 4: Сохранение в SQLite**  
1. Создаем `database/db.py`:  
   ```python
   import sqlite3

   def init_db():
       conn = sqlite3.connect("users.db")
       cursor = conn.cursor()
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               name TEXT,
               email TEXT
           )
       """)
       conn.commit()
       conn.close()

   def add_user(user_id: int, name: str, email: str):
       conn = sqlite3.connect("users.db")
       cursor = conn.cursor()
       cursor.execute("INSERT INTO users (user_id, name, email) VALUES (?, ?, ?)", (user_id, name, email))
       conn.commit()
       conn.close()
   ```
2. Обновляем `process_email` в `handlers/user.py`:  
   ```python
   from database.db import add_user

   @router.message(F.state == "waiting_email")
   async def process_email(message: Message, state: FSMContext):
       data = await state.get_data()
       add_user(message.from_user.id, data['name'], message.text)
       await message.answer("Данные сохранены! Напиши /profile, чтобы посмотреть профиль.")
       await state.clear()
   ```

---

### **📌 Шаг 5: Команда /profile**  
Добавляем в `handlers/user.py`:  
```python
from database.db import get_user

@router.message(F.text == "/profile")
async def cmd_profile(message: Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer(f"Твой профиль:\nИмя: {user[1]}\nEmail: {user[2]}")
    else:
        await message.answer("Ты не зарегистрирован! Напиши /start.")
```

---

### **📌 Шаг 6: Админ-панель**  
1. В `handlers/admin.py`:  
   ```python
   from aiogram import Router, F
   from aiogram.types import Message
   from database.db import get_all_users

   router = Router()

   @router.message(F.text == "/admin")
   async def cmd_admin(message: Message):
       if message.from_user.id == int(os.getenv("ADMIN_ID")):
           users = get_all_users()
           response = "Список пользователей:\n"
           for user in users:
               response += f"{user[0]}: {user[1]} ({user[2]})\n"
           await message.answer(response)
       else:
           await message.answer("Ты не админ!")
   ```
2. Подключаем в `main.py`:  
   ```python
   from handlers.admin import router as admin_router
   dp.include_router(admin_router)
   ```

---

### **🚀 Запуск и тестирование**  
1. Пишем `/start` → регистрируемся.  
2. Проверяем `/profile`.  
3. Админ пишет `/admin` → видит список юзеров.  

---

### **🔜 Что дальше?**  
- Добавить кнопки (InlineKeyboard) вместо текстовых команд.  
- Перейти с SQLite на PostgreSQL.  
- Настроить Webhook для деплоя.  

Если все работает — пиши, идем дальше! 😊  

**Ссылки:**  
- [Aiogram 3.x Documentation](https://docs.aiogram.dev/)  
- [Код этого воркшопа на GitHub](https://github.com/aiogram/bot-tutorial) (аналоги)  

Готов продолжить? Или хочешь доработать текущий бот?