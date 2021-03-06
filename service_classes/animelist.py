from data_scraping.scraper import Scraper
from typing import List
from data_scraping.datasource import DataSource


class AnimeListResult:

    def __init__(self, title: str, anime_id: str, anime_type: str):
        self.title = title
        self.anime_id = str(anime_id)
        self.type = anime_type


class AnimeList:

    def __init__(self, data: DataSource):
        self.__data = data

    def fetch(self, user: str) -> List:
        data = self.__data.fetch(user)
        return [AnimeListResult(*x) for x in data]
