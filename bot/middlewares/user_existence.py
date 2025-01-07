from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select
from db import User


class CheckUserExistence(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = await data["db_session"].scalar(select(User).where(User.id == event.from_user.id))
        
        if not user:
            user = User(id=event.from_user.id)
            data["db_session"].add(user)
            await data["db_session"].commit()
        return await handler(event, data)