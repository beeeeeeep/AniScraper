import re
from difflib import SequenceMatcher
from typing import List

import anitopy

from data_scraping.datasource import DataSource


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
    def __parse_size(size: str) -> float:
        if "MiB" in size:
            return float(size.split(" ")[0]) / 1000
        if "GiB" in size:
            return float(size.split(" ")[0])
        return 0

    @staticmethod
    def __string_closeness(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def rank(data: List[IndexerResult], title: str, pref_groups: List[str], pref_quality: str, season: int,
             min_gib: int = None, prefer_bluray: bool = True) -> List[IndexerResult]:
        ranks = {}
        for entry in data:
            size = Indexer.__parse_size(entry.size)
            if size < min_gib:
                continue
            parse = anitopy.parse(entry.title)
            if parse.get("anime_season") is not None and parse["anime_season"] != str(season):
                continue
            if isinstance(parse.get("episode_number", None), str):
                # singular episode
                if not (parse.get("episode_title") is not None and re.sub(r"[^a-zA-Z0-9]*", "",
                                                                          parse["episode_title"]).isnumeric()):
                    # Fixes batch formats like 01 ~ 12
                    continue
            rank = 0
            if parse.get("release_group") is not None and parse["release_group"].lower() in pref_groups:
                rank += 1
            if parse.get("video_resolution") is not None and pref_quality.replace("p", "") in parse[
                "video_resolution"].lower():
                rank += 1
            if prefer_bluray and parse.get("source") is not None and any(
                    x in parse["source"].lower() for x in ["bd", "blu"]):
                rank += 1
            rank *= Indexer.__string_closeness(title.lower(), parse["anime_title"].lower())
            ranks[entry] = rank
        return [k for k, v in sorted(ranks.items(), key=lambda x: x[1])]

    def query(self, name: str) -> List[IndexerResult]:
        data = self.__data.fetch(name)
        return [IndexerResult(*x) for x in data]
