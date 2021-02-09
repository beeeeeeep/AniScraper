from data_scraping.scraper import Scraper


class Identification:

    def __init__(self, scraper: Scraper):
        self.__scraper = scraper

    def search(self, query: str) -> str:
        """Returns a unique ID for an anime title"""

        