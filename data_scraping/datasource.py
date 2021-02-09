from abc import ABC, abstractmethod
from data_scraping.api import APIParser
from data_scraping.scraper import Scraper
from typing import Callable, List


class DataSource(ABC):

    def __init__(self, query_formatter: Callable[[str], str]):
        self.__query_formatter = query_formatter

    @abstractmethod
    def fetch(self, query: str) -> List[str]:
        pass


class WebScrapeSource(DataSource):

    def __init__(self, query_formatter: Callable[[str], str], scraper: Scraper):
        self.__scraper = scraper
        super().__init__(query_formatter)

    def fetch(self, query: str) -> List[str]:
        return self.__scraper.scrape(self.__query_formatter(query))


class APISource(DataSource):

    def __init__(self, query_formatter: Callable[[str], str], request_parser: APIParser):
        self.__request_parser = request_parser
        super().__init__(query_formatter)

    def fetch(self, query: str) -> List[str]:
        return self.__request_parser.fetch(self.__query_formatter(query))
