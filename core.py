from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_reader import config


bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(), 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

_engine = create_async_engine(url=config.DB_URL.get_secret_value())
_sessionmaker = async_sessionmaker(bind=_engine, expire_on_commit=False) 