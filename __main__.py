import uvicorn
import logging_config

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from bot.handlers import setup_routers
from bot.middlewares import DBSessionMiddleware, CheckUserExistence, SchedulerMiddleware

from db import Base
from config_reader import config
from tuna_manager import stop_tuna
from web.auth.api_router import router
from core import bot, _engine, _sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    webhook_url = f"{config.WEBHOOK_URL.get_secret_value()}/webhook"
    webhook_pid = config.WEBHOOK_PID
    webapp_pid = config.WEBAPP_PID
    
    await bot.set_webhook(
        url=f"{webhook_url}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    
    scheduler.start()
    
    async with _engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        
    yield
    
    scheduler.shutdown()
    stop_tuna(webhook_pid)
    stop_tuna(webapp_pid)
    
    await bot.delete_webhook(True)
    await bot.session.close()
    await _engine.dispose()


dp = Dispatcher(storage=MemoryStorage())

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kworkhunter-webapp.ru.tuna.am",
        "https://kworkhunter-test-webapp.ru.tuna.am"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

dp.message.middleware.register(DBSessionMiddleware(_sessionmaker))
dp.callback_query.middleware.register(DBSessionMiddleware(_sessionmaker))
dp.message.middleware.register(CheckUserExistence())
dp.callback_query.middleware.register(CheckUserExistence())
dp.message.middleware.register(SchedulerMiddleware(scheduler))
dp.callback_query.middleware.register(SchedulerMiddleware(scheduler))
dp.include_router(setup_routers())
    

@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.WEBHOOK_PORT)



