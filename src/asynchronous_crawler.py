import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import re
from src import settings
from src.utility import Utility


class AsynchronousCrawler:
    """
    Crawler asynchronously targets potential article pages and ignores all other pages.
    """

    ignored = None
    init_url = None
    max_pages = None
    pattern = None
    visited_urls = None

    def __init__(self):
        self.ignored = 0
        self.init_url = settings.init_url
        self.pattern = re.compile(settings.nyc_regex)
        self.remaining = settings.max_pages
        self.visited_urls = set()

        Utility.reset_cache(settings.cache_directory)

    def start(self):
        """
        Begins the asynchronous crawler.
        """

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.crawler([self.init_url]))
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
        :rtype:    list
        """

        async with aiohttp.ClientSession() as session:
            # with async_timeout.timeout(10): # enable this to prevent accidental DDoS
            async with session.get(url) as response:
                html = await response.text()

                if html != "" and self.pattern.match(url):
                    await self.cache(url, html)

                return self.parse_urls(html)

    def parse_urls(self, html):
        """
        Produces a list of URLs present in the given html.

        :type html: str
        :rtype:     list
        """

        soup = BeautifulSoup(html, "html.parser")
        urls = []

        # (presumably) only in the main page
        for element in soup.findAll("h2", {"class": "section-heading"}):
            if element.a:
                url = element.a.get("href")
                if url not in self.visited_urls:
                    urls.append(Utility.clean_url(url))

        # in main page and appears as relevant articles
        for element in soup.findAll("a", {"class": "story-link"}):
            url = element.get("href")
            if url not in self.visited_urls:
                urls.append(Utility.clean_url(url))

        return urls

    async def cache(self, url, html):
        """
        Asynchronously writes the html contents to local storage.

        :type url:  str
        :type html: str
        :rtype:     list
        """

        file_name = url.replace("https://www.", "").replace(".com", "").replace("/", "-")

        async with aiofiles.open(os.path.join(settings.cache_directory, file_name), 'w') as file:
            try:
                await file.write(html)
            except Exception:
                self.ignored += 1
                print("Number of URLs ignored by Crawler: ", self.ignored)
