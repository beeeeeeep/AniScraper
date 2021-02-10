from data_scraping.scraper import Scraper
from typing import List
from data_scraping.datasource import DataSource


class AnimeList:

    def __init__(self, data: DataSource):
        self.__data = data

    def fetch(self, user: str) -> List:
        return self.__data.fetch(user)
    