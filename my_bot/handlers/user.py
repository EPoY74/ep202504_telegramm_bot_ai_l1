"""
Команды для пользователей
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message


class Form(StatesGroup):
    waiting_name = State()
    waiting_email = State()


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Выводит приглашение дл вввода имени при регистрации
    """
    await message.answer("Для регистрации введите свое имя:")
    #  Устанавливаем состояние
    await state.set_state(Form.waiting_name)


@router.message(StateFilter(Form.waiting_name))
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Ожидает ввод имени при регистрации
    """
    #  Сохраняем имя
    await state.update_data(new_user_name=message.text)
    await message.answer("Введите свой e-mail:")
    #  Устатнавляваю состояние
    await state.set_state(Form.waiting_email)


@router.message(StateFilter(Form.waiting_email))
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Получает электронную почту и приветствует пользователя
    """
    await state.update_data(new_user_email=message.text)
    #  Достает ранее сохраненнуе данные
    new_user_data = await state.get_data()
    await message.answer(
        f"Регистрация завершена!\n"
        f"Вaше имя: {new_user_data['new_user_name']}\n"
        f"Ваш e-mail: {new_user_data['new_user_email']}"
    )
    await state.clear()
