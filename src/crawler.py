from bs4 import BeautifulSoup
from collections import deque
import os
import re
import requests
from src import settings
from src.utility import Utility


class Crawler:
    """
    Crawler targets potential article pages and ignores all other pages.
    """

    ignored = None
    max_pages = None
    pattern = None
    url_queue = None
    visited_pages = None
    visited_urls = None

    def __init__(self):
        self.ignored = 0
        self.max_pages = settings.max_pages
        self.pattern = re.compile(settings.nyc_regex)
        self.url_queue = deque()
        self.url_queue.append(settings.init_url)
        self.visited_pages = 0
        self.visited_urls = set()

        Utility.reset_cache(settings.cache_directory)

    def start(self):
        """
        Main dispatcher of URLs
        """

        while self.visited_pages < self.max_pages:
            if len(self.url_queue) == 0:
                print("Crawling stopped due to URL list exhaustion")
                break

            # Breadth first search
            url = self.url_queue.popleft()

            if url not in self.visited_urls:
                self.crawl(url)

    def crawl(self, url):
        """
        Appends new urls from the web page using class attributes suitable for NYTs. Add tags and attributes here to
        generalize the crawler for other sites.

        :type url: str
        """

        try:
            html = requests.get(url).text
        except requests.exceptions.RequestException as e:
            print(e)
            return

        if html == "":
            return

        if self.pattern.match(url):
            self.cache(url, html)

        self.visited_pages += 1
        self.visited_urls.add(url)

        self.parse_urls(html)

    def parse_urls(self, html):
        """
        Appends new URLs present in the given html too the URL queue.

        :type html: str
        """

        soup = BeautifulSoup(html, "html.parser")

        # this is (presumably) only in the main page
        for element in soup.findAll("h2", {"class": "section-heading"}):
            if element.a:
                url = element.a.get("href")
                if url not in self.visited_urls:
                    self.url_queue.append(Utility.clean_url(url))

        # in main page and appear as relevant articles
        for element in soup.findAll("a", {"class": "story-link"}):
            url = element.get("href")
            if url not in self.visited_urls:
                self.url_queue.append(Utility.clean_url(url))

    def cache(self, url, html):
        """
        Writes the html contents to local storage.

        :type url:  str
        :type html: str
        :rtype:     list
        """

        file_name = url.replace("https://www.", "").replace(".com", "").replace("/", "-")

        with open(os.path.join(settings.cache_directory, file_name), 'w') as file:
            try:
                file.write(html)
            except Exception:
                self.ignored += 1
                print("Number of URLs ignored by Crawler: ", self.ignored)
