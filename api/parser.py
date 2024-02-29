import aiohttp
from bs4 import BeautifulSoup
from threading import Thread
from fake_useragent import UserAgent


class KworkParser():
    
    def __init__(self, session) -> None:
        self.session = session
        self.headers = {
            "Accept": "text/html",
            "User-Agent": UserAgent().random
            }


    async def get_categories(self):
        categories = []
        async with self.session.get(url="https://kwork.ru/manage_kworks", headers=self.headers) as response:
            soup = BeautifulSoup(response, "lxml")
            result = soup.find('//*[@id="body"]/div[6]/div[1]/div[2]/div[1]/ul[1').text
            print(result)
        return categories
    
    
    async def get_subcategories(self, category):
        subcategories = []
        return subcategories
    
    
    async def parse_kwork(self, message, subcategory):
        pass
        # async with self.session.get(url="https://service.urentbike.ru/gatewayclient/api/v1/payment/profile",
        #                                 headers=(access_headers or self.access_headers)) as response_payment_profile:
        #         return await response_payment_profile.json()


async def run_parse(message):
    async with aiohttp.ClientSession() as session:
        parser = KworkParser(session=session)
        for cat in await parser.get_categories():
            for subcat in await parser.get_subcategories(cat):
                th = Thread(target=parser.parse_kwork, args=(message, subcat,))
                th.start()
        