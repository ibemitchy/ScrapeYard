import asyncio
from Crawler import Crawler
from CrawlerAsync import CrawlerAsync
from collections import deque
from Scraper import Scraper


def scrape_yard():
    max_pages = 100
    # init_url = "https://www.nytimes.com/"
    init_url = "https://ibemitchy.github.io/"

    # unscientific 100 URLs benchmark (150Mbps internet):
    # synchronous:  ~35 seconds
    # asynchronous:  ~9 seconds

    async = True

    crawler = CrawlerAsync(init_url, max_pages) if async else Crawler(init_url, max_pages)
    crawler.start()

    # scraper = Scraper(list(crawler.get_urls()))
    # scraper = Scraper(["https://www.nytimes.com/2018/01/11/science/climate-change-lakes-streams.html"])

    # scraper.start()
    # print(crawler.get_urls())


if __name__ == "__main__":
    scrape_yard()
