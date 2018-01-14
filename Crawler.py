from bs4 import BeautifulSoup
from collections import deque
import requests


class Crawler:
    """
    Crawler targets potential article pages and ignores all other pages.
    """

    __init_url = None
    __max_pages = None
    __visited_pages = None
    __url_queue = None
    __visited_url = None

    def __init__(self, init_url, max_pages):
        self.__init_url = init_url
        self.__max_pages = max_pages
        self.__visited_pages = 0
        self.__url_queue = deque()
        self.__url_queue.append(init_url)
        self.__visited_url = set()

    def start(self):
        """
        Main dispatcher of URLs
        """

        while self.__visited_pages < self.__max_pages:
            if len(self.__url_queue) == 0:
                print("Crawling stopped after URL list is exhausted")
                break

            # Breadth first search
            url = self.__url_queue.popleft()

            if url not in self.__visited_url:
                self.__crawl(url)

    def __crawl(self, url):
        """
        Appends new urls from the web page using class attributes suitable for NYTs. Add tags and attributes here to
        generalize the crawler for other sites.
        :type url: str
        """
        try:
            data = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return

        self.__visited_pages += 1
        self.__visited_url.add(url)
        soup = BeautifulSoup(data.text, "html.parser")

        # this is (presumably) only in the main page
        for element in soup.findAll("h2", {"class": "section-heading"}):
            if element.a:
                self.__url_queue.append(element.a.get("href"))

        # in main page and appear as relevant articles
        for element in soup.findAll("a", {"class": "story-link"}):
            self.__url_queue.append(element.get("href"))

    def get_urls(self):
        return self.__visited_url

