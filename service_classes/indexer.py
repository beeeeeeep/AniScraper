import itertools
import logging
import re
import textdistance
from typing import List

import anitopy

from data_scraping.datasource import DataSource
from implementations.search.anilist import search


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
        return textdistance.levenshtein.normalized_similarity(a, b)

    @staticmethod
    def rank(data: List[IndexerResult], anilist_id: int, titles: List[str], pref_groups: List[str], pref_quality: str,
             season: int, min_gib: int = None, prefer_bluray: bool = True, min_seeders: int = 0,
             seeders_importance: float = 1, return_ranks: bool = False) -> List[IndexerResult]:
        # TODO: make nicer
        EPISODE_NUMBER_EXCEPTIONS = ["539"]
        BATCH_KEYWORDS = ["batch", "complete", "season", rf"S0*{season}", r"1 ?-|~ ?[1-3][0-9]"]
        if season < 1:
            raise ValueError("Season cannot be less than one")
        ranks = {}
        anitopy_parse = [(x, anitopy.parse(x.title)) for x in data]
        max_seeders = max(x.seeders for x in data)
        mismatched_anime_ids = {}
        for entry, parse in anitopy_parse:
            if entry.seeders < min_seeders:
                continue
            if re.search(r"\([0-9]{4}.*\)", parse["anime_title"]) is not None:
                parse["anime_title"] = re.sub(r"\([0-9]{4}.*\)", "", parse["anime_title"])
            if re.search(rf"S0*{season}", parse["anime_title"]) is not None:
                parse["anime_title"] = re.sub(rf"S0*{season}", "", parse["anime_title"])
            if any(f"season {x}" in entry.title.lower() for x in range(1, 100) if x != season):
                # missed case by anitopy season parsing
                continue
            size = Indexer.__parse_size(entry.size)
            if size < min_gib:
                continue
            if parse.get("anime_season") is not None:
                if isinstance(parse["anime_season"], str) and int(parse["anime_season"]) != season:
                    continue
                if isinstance(parse["anime_season"], list) and season not in [int(x) for x in parse["anime_season"]]:
                    continue
            if isinstance(parse.get("episode_number", None), str) and parse[
                "episode_number"] not in EPISODE_NUMBER_EXCEPTIONS:
                # ignore singular episode
                if not (parse.get("episode_title") is not None and re.sub(r"[^a-zA-Z0-9]*", "",
                                                                          parse["episode_title"]).isnumeric()):
                    # Fixes batch formats like 01 ~ 12
                    continue
            rank = 0
            if parse.get("release_group") is not None and parse["release_group"].lower() in [x.lower() for x in pref_groups]:
                rank += 1
            if parse.get("video_resolution") is not None and pref_quality.replace("p", "") in parse[
                "video_resolution"].lower():
                rank += 2
            is_bluray = False
            if prefer_bluray and parse.get("source") is not None:
                if isinstance(parse["source"], str):
                    source = parse["source"]
                elif isinstance(parse["source"], list):
                    source = " ".join(parse["source"])
                else:
                    raise Exception("Hopefully not possible")
                if any(x in source.lower() for x in ["bd", "blu"]):
                    rank += 2
                    is_bluray = True
            if any(re.search(x, entry.title.lower(), re.IGNORECASE) for x in BATCH_KEYWORDS) or is_bluray:
                rank += 2
            title_similarity = max(Indexer.__string_closeness(x.lower(), parse["anime_title"].lower()) for x in titles)
            if title_similarity < 0.5:
                continue
            if title_similarity < 0.8:
                a_id = -1
                for k, v in mismatched_anime_ids.items():
                    if Indexer.__string_closeness(k, parse["anime_title"]) > 0.8:
                        a_id = v
                        break
                if a_id == -1:
                    logging.debug(f"Unsure about {parse['anime_title']}, doing anilist ID search")
                    a_id = search.fetch(parse["anime_title"], sort="TITLE_ROMAJI")[0]
                    mismatched_anime_ids[parse["anime_title"]] = a_id
                if a_id != anilist_id:
                    continue
            rank *= 1 + (entry.seeders / max_seeders) * seeders_importance
            ranks[entry] = rank
        if not return_ranks:
            return [k for k, v in reversed(sorted(ranks.items(), key=lambda x: x[1]))]
        # special debug case
        return [(k, v) for k, v in reversed(sorted(ranks.items(), key=lambda x: x[1]))]

    def query(self, name: str) -> List[IndexerResult]:
        data = self.__data.fetch(name)
        return [IndexerResult(*x) for x in data]
