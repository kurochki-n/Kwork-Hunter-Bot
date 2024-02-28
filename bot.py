import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers.user import router as user_router
from loader import loop


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(funcName)s) %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
    )

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False) 


if __name__ == "__main__":
    loop.run_until_complete(main())