from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.utils import tools


class CheckIsAdmin(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        admins = await tools.get_admins()
        
        if event.from_user.id not in admins:
            # executed if the user is not an admin
            ...
            return
        return await handler(event, data)