from bs4 import BeautifulSoup, SoupStrainer
import json
import os
from multiprocessing import Pool
from src import settings
from src.utility import Utility


class MultiprocessScraper:
    """
    Scraper extracts basic information from cached HTML files with multiple processes.
    """

    files = None
    __nyc_reg = None

    def __init__(self):
        self.nyc_regex = settings.nyc_regex
        try:
            self.files = [file for file in os.listdir(settings.cache_directory)]
        except FileNotFoundError:
            print("Nothing to scrape")
            self.files = []

        Utility.reset_cache(settings.output_directory)

    def start(self):
        """
        Sets up the processes.
        """

        pool = Pool(processes=settings.cpu_count)
        pool.map(MultiprocessScraper.scraper, self.files)
        pool.close()
        pool.join()

    @staticmethod
    def scraper(file_name):
        """
        Opens and scrapes the HTML file.
        """

        file_loc = os.path.join(settings.cache_directory, file_name)
        with open(file_loc) as file:
            html = file.read()
            MultiprocessScraper.scrape(file_name, html)

    @staticmethod
    def scrape(file_name, html):
        """
        Scrapes the given HTML.
        """

        with open(os.path.join(settings.output_directory, file_name).replace(".html", ".json"), "w") as file:
            file.write(html)

        strainer = SoupStrainer(["span", "h1", "p"])
        soup = BeautifulSoup(html, "html.parser", parse_only=strainer)

        try:
            author = soup.find("span", {"class": "byline-author"}).getText().title()
            date = Utility.clean_date(soup.find("time", {"class": "dateline"}).get("datetime"))
            title = soup.find("h1", {"id": "headline"}).getText()

            # appends article bodies
            content = []
            for para in soup.findAll("p", {"class": "story-content"}):
                content.append(para.getText())

            # article = Article(author, content, date, title)
            # print(article.to_string())

            with open(os.path.join(settings.output_directory, file_name).replace(".html", ".json"), "w") as file:
                article = {
                    "author": author,
                    "content": content,
                    "date": date,
                    "title": title,
                }

                json.dump(article, file, indent=4, ensure_ascii=False)

        except AttributeError:
            pass
