from os import stat
import re
from typing import Callable, List, Tuple, Dict
import requests
from scraper import Scraper


class Indexer:

    def __init__(self, url: str, fields_format: Callable[[str], str], scraper: Scraper):
        self.url = url
        self.scraper = scraper
        self.fields_format = fields_format

    @staticmethod
    def rank(data: List[Dict], pref_groups: List[str], pref_quality: str, keywords: List[str], type: str, min_gib: int = None, prefer_first_season: bool = False) -> List:
        ACCEPTABLE_KEYS = ["title", "link", "seeders", "size"]
        for entry in data:
            entry["seeders"] = int(entry["seeders"])
            if list(entry.keys()) != ACCEPTABLE_KEYS:
                raise TypeError(f"Expected keys {', '.join(ACCEPTABLE_KEYS)}")
        if min_gib is not None:
            data = [x for x in data if all(y not in x["size"].lower() for y in ["mib", "kib"]) and float(x["size"].lower().replace(" gib", "")) > min_gib]
        for entry in data:
            rank = 0
            if any(x.lower() in entry["title"].lower() for x in pref_groups):
                rank += 1
            if any(x.lower() in entry["title"].lower() for x in keywords):
                rank += 1
            if pref_quality.lower() in entry["title"].lower():
                rank += 1
            if type == "TV" and "movie" in entry["title"].lower():
                rank -= 10
            if entry["seeders"] < 4:
                rank -= 10
            if prefer_first_season and re.match(r"^.* [2-9] [\[\(\-].*$", entry["title"]):
                rank -= 2
            entry["rank"] = rank
        data.sort(key=lambda x: x["rank"], reverse=True)
        highest_ranked = [x for x in data if x["rank"] == data[0]["rank"]]
        highest_ranked.sort(key=lambda x: x["seeders"], reverse=True)
        return highest_ranked
            

    def query(self, name: str) -> List:
        name = name.replace(" ", "+")
        try:
            data = self.scraper.scrape(self.url + self.fields_format(name))
        except ConnectionError:
            raise ConnectionError(f"Could not connect to indexer {self.url}")
        return data
    