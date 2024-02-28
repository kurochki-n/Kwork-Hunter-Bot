import requests
from bs4 import BeautifulSoup

from loader import loop


bs = BeautifulSoup()

async def parse_kwork():
    pass


async def run_parse():
    loop.create_task(parse_kwork())