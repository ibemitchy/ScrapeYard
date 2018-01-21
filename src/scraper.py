from bs4 import BeautifulSoup, SoupStrainer
import json
import os
from src import settings
from src.utility import Utility


class Scraper:
    """
    Scraper extracts basic information from cached HTML files in a single process.
    """

    files = None

    def __init__(self):
        try:
            self.files = [file for file in os.listdir(settings.cache_directory)]
        except FileNotFoundError:
            print("Nothing to scrape")

        Utility.reset_cache(settings.output_directory)

    def start(self):
        """
        Retrieves the HTML content for scraping.
        """

        for file_name in self.files:
            file_loc = os.path.join(settings.cache_directory, file_name)

            with open(file_loc) as file:
                html = file.read()
                Scraper.scrape(file_name, html)

    @staticmethod
    def scrape(file_name, html):
        """
        Scrapes the given HTML.
        """

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
