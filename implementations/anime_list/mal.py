from data_scraping.datasource import WebScrapeSource
from animelist import AnimeList
import json
import os
import re
import time
from data_scraping.scraper import Scraper, SubelementSelector


def mal_json_parser(raw: str) -> str:
    data = json.loads(raw)
    return [(re.sub(r"\(TV\)|\(Movie\)|\(OVA\)", "", x["anime_title"], flags=re.IGNORECASE), x["anime_id"], x["anime_media_type_string"], x["anime_season"]["year"]) for x in data]

ptw = AnimeList(
    WebScrapeSource(
        query_formatter=lambda x: f"https://myanimelist.net/animelist/{x}?status=6",
        scraper=Scraper(
            parser="lxml",
            root=["table", ["list-table"]],
            subelem_selectors=[
                SubelementSelector([], attribute="data-items")
            ],
            map=mal_json_parser,
            postprocess=lambda x: x[0][0]
        )
    )
)
