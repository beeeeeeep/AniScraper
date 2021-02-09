from typing import Callable, List, Tuple, Union
from bs4 import BeautifulSoup
import requests


class SubelementSelector:

    def __init__(self, subelem_path: List[Union[Tuple[str, List[str]], Tuple[str, List[str], int]]], attribute: str):
        self.subelem_path = subelem_path
        self.attribute = attribute

    def select(self, parent: BeautifulSoup) -> str:
        for selector in self.subelem_path:
            tag = selector[0]
            classes = selector[1]
            if len(selector) == 2:
                parent = parent.find(tag, classes)
            else:
                parent = parent.find_all(tag, classes)[selector[2]]
        if self.attribute == "text":
            return parent.getText()
        return parent[self.attribute]


class Scraper:

    def __init__(self, parser: str, root: Tuple[str, List[str]], subelem_selectors: List[SubelementSelector] = [], map: Callable[[str], str] = None, postprocess: Callable[[List], str] = None):
        self.parser = parser
        self.root = root
        self.subelem_selectors = subelem_selectors
        self.map = map if map is not None else lambda x: x
        self.postprocess = postprocess if postprocess is not None else lambda x: x

    def scrape(self, url: str) -> List:
        r = requests.get(url)
        if r.status_code != 200:
            raise ConnectionError("Could not GET url")
        soup = BeautifulSoup(r.text, self.parser)
        elements = soup.find_all(self.root[0], self.root[1])
        subelements = []
        for elem in elements:
            group = []
            for selector in self.subelem_selectors:
                group.append(self.map(selector.select(elem)))
            subelements.append(group)
        return self.postprocess(subelements)


# class Search(Scraper):

#     def __init__(self, query_str: Callable[[str], str], parser: str, root: Tuple[str, List[str]], subelem_selectors: List[SubelementSelector] = [], map: Callable[[str], str] = None, postprocess: Callable[[List], str] = None):
#         self.query_str = query_str
#         super().__init__(parser, root, subelem_selectors=subelem_selectors, map=map, postprocess=postprocess)

#     def search(self, query: str) -> str:
#        return self.scrape(self.query_str(query)) 
