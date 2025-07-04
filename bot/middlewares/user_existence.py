from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select
from db import User, KworkSession


class CheckUserExistence(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = await data["db_session"].scalar(select(User).where(User.id == event.from_user.id))
        
        if not user:
            user = User(
                id=event.from_user.id,
                username=event.from_user.username,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name
            )
            data["db_session"].add(user)
            kwork_session = KworkSession(user_id=user.id)
            data["db_session"].add(kwork_session)
            await data["db_session"].commit()
            
        return await handler(event, data)
