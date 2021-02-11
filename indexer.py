from data_scraping.datasource import DataSource
from os import stat
import re
from typing import Callable, List, Tuple, Dict
import requests
from collections import Counter


class IndexerResult:

    def __init__(self, title: str, link: str, seeders: int, size: str):
        self.title = title
        self.link = link
        self.seeders = int(seeders)
        self.size = size


class Indexer:

    def __init__(self, data: DataSource):
        self.__data = data

    @staticmethod
    def rank(data: List[IndexerResult], pref_groups: List[str], pref_quality: str, keywords: List[str], type: str, min_gib: int = None, prefer_first_season: bool = False) -> List[IndexerResult]:
        if min_gib is not None:
            data = [x for x in data if all(y not in x.size.lower() for y in ["mib", "kib"]) and float(x.size.lower().replace(" gib", "")) > min_gib]
            if len(data) == 0:
                return []
        count = Counter()
        for entry in data:
            rank = 0
            if any(x.lower() in entry.title.lower() for x in pref_groups):
                rank += 1
            if any(x.lower() in entry.title.lower() for x in keywords):
                rank += 1
            if pref_quality.lower() in entry.title.lower():
                rank += 1
            if type == "TV" and "movie" in entry.title.lower():
                rank -= 10
            if entry.seeders < 4:
                rank -= 10
            if prefer_first_season and re.match(r"^.* [2-9] [\[\(\-].*$", entry.title):
                rank -= 2
            count[entry] = rank
        highest_ranked = [x[0] for x in count.most_common() if x[1] == count.most_common(1)[0][1]]
        highest_ranked.sort(key=lambda x: x.seeders, reverse=True)
        second = [x[1] for x in count.most_common() if x[1] != count.most_common(1)[0][1]]
        if len(second) > 0:
            second_count = second[0]
            second_highest_rank = [x[0] for x in count.most_common() if x[1] == second_count]
            second_highest_rank.sort(key=lambda x: x.seeders, reverse=True)
            if second_highest_rank[0].seeders > highest_ranked[0].seeders * 5:
                return second_highest_rank
        return highest_ranked
            
    def query(self, name: str) -> List[IndexerResult]:
        data = self.__data.fetch(name)
        return [IndexerResult(*x) for x in data]
    