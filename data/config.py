import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT'))
MYSQL_LOGIN = os.getenv('MYSQL_LOGIN')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_NAME = os.getenv('MYSQL_NAME')