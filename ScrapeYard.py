
from Crawler import Crawler
from collections import deque
from Scraper import Scraper


def scrape_yard():
    max_pages = 100
    init_url = "https://www.nytimes.com/"

    # crawler = Crawler(init_url, max_pages)
    # crawler.start()


    # scraper = Scraper(list(crawler.get_urls()))
    scraper = Scraper(["https://www.nytimes.com/2018/01/11/science/climate-change-lakes-streams.html"])

    scraper.start()
    # print(crawler.get_urls())


if __name__ == "__main__":
    scrape_yard()
