import re


class AnimeInfo:
    def __init__(self, episode: int, batch: bool, title: str, year: int, _type: str, quality: str, encoding: str, bdrip: bool,
                 group: str, season: int):
        self.episode = episode
        self.batch = batch
        self.title = title
        self.year = year
        self._type = _type
        self.quality = quality
        self.encoding = encoding
        self.bdrip = bdrip
        self.group = group
        self.season = season


def parse_filename(filename: str) -> AnimeInfo:
    brackets = re.findall(r"\[[^]]*]|\([^)]*\)", filename)
    for bracket in brackets:

    clean_filename = re.sub(r"\[.*]|\(.*\)", "", filename).strip()
