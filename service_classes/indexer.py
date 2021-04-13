import re
import textdistance
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
        # TODO: determine best similarity metric
        return textdistance.hamming.normalized_similarity(a, b)

    @staticmethod
    def rank(data: List[IndexerResult], title: str, pref_groups: List[str], pref_quality: str, season: int,
             min_gib: int = None, prefer_bluray: bool = True, min_seeders: int = 0, seeders_importance: float = 1,
             return_ranks: bool = False) -> List[IndexerResult]:
        # TODO: fix eng titles
        EPISODE_NUMBER_EXCEPTIONS = ["539"]
        if season < 1:
            raise ValueError("Season cannot be less than one")
        ranks = {}
        anitopy_parse = [(x, anitopy.parse(x.title)) for x in data]
        for entry, parse in anitopy_parse:
            if entry.seeders < min_seeders:
                continue
            if any(f"season {x}" in entry.title.lower() for x in range(1, 100) if x != season):
                # missed case by anitopy season parsing
                continue
            size = Indexer.__parse_size(entry.size)
            if size < min_gib:
                continue
            if parse.get("anime_season") is not None:
                if isinstance(parse["anime_season"], str) and parse["anime_season"] != str(season):
                    continue
                if isinstance(parse["anime_season"], list) and str(season) not in parse["anime_season"]:
                    continue
            if isinstance(parse.get("episode_number", None), str) and parse[
                "episode_number"] not in EPISODE_NUMBER_EXCEPTIONS:
                # ignore singular episode
                if not (parse.get("episode_title") is not None and re.sub(r"[^a-zA-Z0-9]*", "",
                                                                          parse["episode_title"]).isnumeric()):
                    # Fixes batch formats like 01 ~ 12
                    continue
            rank = 0
            if parse.get("release_group") is not None and parse["release_group"].lower() in pref_groups:
                rank += 1
            if parse.get("video_resolution") is not None and pref_quality.replace("p", "") in parse[
                "video_resolution"].lower():
                rank += 2
            if prefer_bluray and parse.get("source") is not None:
                if isinstance(parse["source"], str):
                    source = parse["source"]
                elif isinstance(parse["source"], list):
                    source = " ".join(parse["source"])
                else:
                    raise Exception("Hopefully not possible")
                if any(x in source.lower() for x in ["bd", "blu"]):
                    rank += 2
            title_similarity = Indexer.__string_closeness(title.lower(), parse["anime_title"].lower())
            if title_similarity < 0.5:
                continue
            rank *= title_similarity
            rank += entry.seeders * seeders_importance
            ranks[entry] = rank
        if not return_ranks:
            return [k for k, v in reversed(sorted(ranks.items(), key=lambda x: x[1]))]
        # special debug case
        return [(k, v) for k, v in reversed(sorted(ranks.items(), key=lambda x: x[1]))]

    def query(self, name: str) -> List[IndexerResult]:
        data = self.__data.fetch(name)
        return [IndexerResult(*x) for x in data]
