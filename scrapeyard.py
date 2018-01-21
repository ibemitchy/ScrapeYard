from src.crawler import Crawler
from src.asynchronous_crawler import AsynchronousCrawler
from src.scraper import Scraper
from src.multiprocess_scraper import MultiprocessScraper
from src import settings


def scrape_yard():
    crawler = AsynchronousCrawler() if settings.isASynchronous else Crawler()
    crawler.start()

    scraper = MultiprocessScraper() if settings.isMultiprocess else Scraper()
    scraper.start()


if __name__ == "__main__":
    scrape_yard()
