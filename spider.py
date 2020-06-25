import asyncio
import aiohttp
from bs4 import BeautifulSoup
from headers_pool import User_Agent
import random
import time


# 访问页面 返回soup
class Downloader:
    def __init__(self, urls):
        self.urls = urls
        self._soups = []
        self.user_agents = User_Agent()
        self.user_agent = random.choice(self.user_agents.user_agents)
        self.headers = {'User-Agent': self.user_agent}

    async def download_page(self, url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                self._soups.append(soup)

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.download_page(url)) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def soups(self):
        self.download()
        return self._soups
