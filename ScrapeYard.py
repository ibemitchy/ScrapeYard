from Crawler import Crawler
from Scraper import Scraper


def scrape_yard():
    max_pages = 100
    init_url = "https://www.nytimes.com/"

    crawler = Crawler(init_url, max_pages)
    crawler.start()
    scraper = Scraper(list(crawler.get_urls()))
    scraper.start()
    # print(crawler.get_urls())


if __name__ == "__main__":
    scrape_yard()
