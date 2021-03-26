from data_scraping.scraper import Scraper
from typing import List
from data_scraping.datasource import DataSource


class AnimeListResult:

    def __init__(self, title: str, anime_id: str, type: str, year: int):
        self.title = title
        self.anime_id = str(anime_id)
        self.type = type
        self.year = int(year)


class AnimeList:

    def __init__(self, data: DataSource):
        self.__data = data

    def fetch(self, user: str) -> List:
        data = self.__data.fetch(user)
        return [AnimeListResult(*x) for x in data]
