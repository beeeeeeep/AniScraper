import re
from typing import Optional, List


class AnimeInfo:
    def __init__(self, episode: Optional[int], batch: bool, title: str, quality: str,
                 encoding: List[str], bdrip: bool, group: Optional[str], season: int):
        self.episode = episode
        self.batch = batch
        self.title = title
        self.quality = quality
        self.encoding = encoding
        self.bdrip = bdrip
        self.group = group
        self.season = season


def parse_filename(filename: str) -> AnimeInfo:
    brackets = re.findall(r"\[[^]]*]|\([^)]*\)", filename)
    clean_filename = re.sub(r"\[.*]|\(.*\)", "", filename).strip()
    return AnimeInfo(
        episode=1,
        batch=False,
        title="lmao",
        quality="no",
        encoding=[],
        bdrip=True,
        group=None,
        season=0
    )
