import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio

class KworkParser():
    
    def __init__(self, session) -> None:
        self.session = session
        self.headers = {
            "Accept": "text/html",
            "User-Agent": UserAgent().random
            }


    async def get_categories(self):
        async with self.session.get(url="https://kwork.ru/categories", headers=self.headers) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            result = soup.find_all("h2", {"class": "categories-item__title not-h2 js-categories-collapse-header"})
            
            categories = []
            for element in result:
                categories.append(element.text)
            return categories
    
    
    async def get_subcategories_by_category(self, category):
        async with self.session.get(url="https://kwork.ru/categories", headers=self.headers) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            result = soup.find("div", {"class": "all-categories"}).find_all("div", {"class": "js-categories-collapse-header categories-item__subtitle"})
            
            subcategories = []
            for element in result:
                subcategories.append(element.text)
            return subcategories
    
    
    async def get_all_subcategories(self):
        async with self.session.get(url="https://kwork.ru/categories", headers=self.headers) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            result = soup.find("div", {"class": "all-categories"}).find_all("div", {"class": "js-categories-collapse-header categories-item__subtitle"})
            
            subcategories = []
            for element in result:
                subcategories.append(element.text)
            return subcategories
    
    
    async def parse_kwork(self, message, subcategory):
        pass


async def run_parse(message):
    async with aiohttp.ClientSession() as session:
        parser = KworkParser(session=session)
        
        tasks = []
        for subcat in await parser.get_all_subcategories():
            task = asyncio.create_task(parser.parse_kwork(message, subcat))
            tasks.append(task)
    
        await asyncio.gather(*tasks)
        