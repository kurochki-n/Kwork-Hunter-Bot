import aiomysql
from data import config
from loader import loop

async def connect():
    return await aiomysql.create_pool(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_LOGIN,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_NAME,
        autocommit=True,
        pool_recycle=100
    )
    
db_connect = loop.run_until_complete(connect())