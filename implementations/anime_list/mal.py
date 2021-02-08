import json
import os
import re
import time
from scraper import Scraper, Search, SubelementSelector


def mal_json_parser(raw: str) -> str:
    data = json.loads(raw)
    return [(x["anime_title"], x["anime_id"], x["anime_media_type_string"], x["anime_season"]) for x in data]

ptw = Scraper(
    parser="lxml",
    root=["table", ["list-table"]],
    subelem_selectors=[
        SubelementSelector([], attribute="data-items")
    ],
    map=mal_json_parser,
    postprocess=lambda x: x[0][0]
)

search = Search(
    query_str=lambda x: f"https://myanimelist.net/anime.php?q={x}&cat=anime",
    parser="lxml",
    root=["a", ["hoverinfo_trigger fw-b fl-l"]],
    subelem_selectors=[
        SubelementSelector([], attribute="id")
    ],
    map=lambda x: x.replace("sinfo", ""),
    postprocess=lambda x: x[0][0]
)
