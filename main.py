import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_reader import config
from bot.handlers import setup_routers
from db import Base, _engine


os.makedirs("logs", exist_ok=True)
os.makedirs("temp", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(funcName)s) %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(), 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

scheduler = AsyncIOScheduler()
scheduler.configure(timezone="Europe/Moscow")


async def start_polling() -> None:   
    scheduler.start()
    dp.include_router(setup_routers())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, scheduler=scheduler)
    
    
@dp.startup()
async def on_startup() -> None:
    async with _engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    
    
@dp.shutdown()
async def on_shutdown() -> None:
    await _engine.dispose()
    scheduler.shutdown(wait=False)


if __name__ == "__main__":
    asyncio.run(start_polling())
