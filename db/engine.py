from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_reader import config


_engine = create_async_engine(url=config.DB_URL.get_secret_value())
_sessionmaker = async_sessionmaker(bind=_engine, expire_on_commit=False)
