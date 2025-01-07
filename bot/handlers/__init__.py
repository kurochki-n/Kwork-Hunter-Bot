from aiogram import Router

from . import user_router


def setup_routers() -> Router:
    router = Router()
    
    router.include_router(user_router.router)
    return router
