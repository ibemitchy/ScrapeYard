import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
import time


class CrawlerAsync:
    """
    Crawler asynchronously targets potential article pages and ignores all other pages.
    """

    init_url = None
    max_pages = None
    visited_urls = None

    def __init__(self, init_url, max_pages):
        self.init_url = init_url
        self.remaining = max_pages
        self.visited_urls = set()

    def start(self):
        """
        Begins the asynchronous crawler.
        """

        loop = asyncio.get_event_loop()
        # start_time = time.time()
        loop.run_until_complete(self.crawler([self.init_url]))
        # print(time.time() - start_time)
        loop.close()

    async def crawler(self, urls):
        """
        Crawls through the given URLs and spawns another crawlers.

        :type urls: list
        """

        length = min(len(urls), self.remaining)

        if length <= 0:
            return

        urls = urls[:length]
        self.remaining -= length
        self.visited_urls |= set(urls)

        lists_of_urls = [asyncio.ensure_future(self.fetch_urls(url)) for url in urls]
        lists_of_urls = await asyncio.gather(*lists_of_urls)
        urls = [url for urls in lists_of_urls for url in urls]
        await asyncio.ensure_future(self.crawler(urls))

    async def fetch_urls(self, url):
        """
        Downloads the html at the given URL and produces a list of URLs inside the html.

        :type url: str
        :rtype: list
        """
        async with aiohttp.ClientSession() as session:
            # with async_timeout.timeout(10): # enable this to prevent accidental DDoS
            async with session.get(url) as response:
                html = await response.text()
                return self.parse_urls(html)

    def parse_urls(self, html):
        """
        Produces a list of URLs present in the given html.

        :type html: str
        :rtype: list
        """

        soup = BeautifulSoup(html, "html.parser")
        urls = []

        # (presumably) only in the main page
        for element in soup.findAll("h2", {"class": "section-heading"}):
            if element.a:
                url = element.a.get("href")
                if url not in self.visited_urls:
                    urls.append(url)

        # in main page and appears as relevant articles
        for element in soup.findAll("a", {"class": "story-link"}):
            url = element.get("href")
            if url not in self.visited_urls:
                urls.append(url)

        return urls

    def get_urls(self):
        return self.visited_urls
