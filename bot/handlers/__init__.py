from aiogram import Router

from . import user_router
from bot.middlewares import CheckUserExistence, DBSessionMiddleware
from db import _sessionmaker


def setup_routers() -> Router:
    router = Router()
    
    router.message.middleware.register(DBSessionMiddleware(_sessionmaker))
    router.callback_query.middleware.register(DBSessionMiddleware(_sessionmaker))
    router.message.middleware.register(CheckUserExistence())
    router.include_router(user_router.router)
    
    return router
