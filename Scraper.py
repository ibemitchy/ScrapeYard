from Article import Article
from bs4 import BeautifulSoup
import re
import requests


class Scraper:
    """
    Scraper filters the URLs and scrapes candidate articles for basic metadata.
    """

    __urls = None
    __nyc_reg = None

    def __init__(self, urls):
        self.__urls = urls
        self.__nyc_regex = "^((http)(s){,1}(://www.)){,1}[A-z]+(.)[A-z]+(/)[\d]{4}(/)[\d]{2}(/)[\d]{2}(/)[^.]*(.html)$"

    def start(self):
        self.__clean_urls()
        while self.__urls:
            Scraper.scrape(self.__urls.pop())

    def __clean_urls(self):
        """
        Cleans the visited URLs by removing reference suffixes and only allowing URLs of a specific form.
        """

        # filter out URL without ".html"
        self.__urls = [url for url in self.__urls if url.find(".html") != -1]

        # remove reference suffixes in URL
        self.__urls = [url[:url.find(".html") + 5] for url in self.__urls]

        # remove non-article URLs
        pattern = re.compile(self.__nyc_regex)
        self.__urls = [url for url in self.__urls if pattern.match(url)]

    @staticmethod
    def scrape(url):
        try:
            data = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return

        soup = BeautifulSoup(data.text, "html.parser")
        author = soup.find("span", {"class": "byline-author"}).getText()
        content = ""
        date = Scraper.clean_date(soup.find("time", {"class": "dateline"}).get("datetime"))
        title = soup.find("h1", {"id": "headline"}).getText()

        for para in soup.findAll("p", {"class": "story-content"}):
            content += para.getText()

        article = Article(author, content, date, title)
        print(article.to_string())

    @staticmethod
    def clean_date(date):
        return date[:date.find("T")]
