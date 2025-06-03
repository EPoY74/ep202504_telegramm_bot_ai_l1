from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select

from ..db import create_async_session
from ..models.user import User

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    from_user = message.from_user
    if from_user is None:
        return
    async for session in create_async_session():
        result = await session.execute(
            select(User).where(User.id == from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                id=from_user.id, full_name=from_user.full_name or "Anonymous"
            )
            session.add(user)
            await session.commit()
        await message.answer(f"Привет, {user.full_name}!")
