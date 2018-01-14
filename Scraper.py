import re


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
        print(self.__urls)

        return 1

    def __clean_urls(self):
        """
        Cleans the visited URLs by removing reference suffixes and only allowing URLs of a specific form.
        """

        # filter out URL without ".html"
        self.__urls = [url for url in self.__urls if url.find(".html") != -1]

        # remove reference suffixes in URL
        self.__urls = [url[:url.find(".html") + 5] for url in self.__urls]

        # remove non-article URLs
        pattern = re.compile(self.__nyc_reg)
        self.__urls = [url for url in self.__urls if pattern.match(url)]
