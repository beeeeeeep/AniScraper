from abc import ABC, abstractmethod
from data_scraping.api import APIParser
from data_scraping.scraper import Scraper
from typing import Callable, List, Dict, Union


class DataSource(ABC):

    def __init__(self, query_formatter: Callable[[str, Dict], Union[str, Dict]]):
        self.query_formatter = query_formatter

    @abstractmethod
    def fetch(self, query: str, **kwargs) -> List[str]:
        pass


class WebScrapeSource(DataSource):

    def __init__(self, query_formatter: Callable[[str], str], scraper: Scraper):
        self.__scraper = scraper
        super().__init__(query_formatter)

    def fetch(self, query: str, **kwargs) -> List[str]:
        return self.__scraper.scrape(self.query_formatter(query))


class APISource(DataSource):

    def __init__(self, url: str, request_type: str, query_formatter: Callable[[str], Dict], request_parser: APIParser):
        self.__url = url
        self.__request_type = request_type
        self.__request_parser = request_parser
        super().__init__(query_formatter)

    def fetch(self, query: str, **kwargs) -> List[str]:
        return self.__request_parser.fetch(url=self.__url, request_type=self.__request_type, data=self.query_formatter(query, kwargs))
