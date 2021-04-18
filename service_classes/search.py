from typing import List
from data_scraping.datasource import DataSource


class Search:

    def __init__(self, data: DataSource):
        self.__data = data

    def fetch(self, query: str, **kwargs) -> List:
        return self.__data.fetch(query, **kwargs)
