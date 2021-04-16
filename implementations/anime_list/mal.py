from datetime import datetime

from data_scraping.datasource import WebScrapeSource
from service_classes.animelist import AnimeList
import json
import re
from data_scraping.scraper import Scraper, SubelementSelector


def mal_json_parser(raw: str) -> list:
    data = json.loads(raw)
    return [
        (
            re.sub(r"\(TV\)|\(Movie\)|\(OVA\)", "", x["anime_title"], flags=re.IGNORECASE),
            x["anime_id"],
            x["anime_media_type_string"]
        ) for x in data]

ptw = AnimeList(
    WebScrapeSource(
        query_formatter=lambda x: f"https://myanimelist.net/animelist/{x}?status=6",
        scraper=Scraper(
            parser="lxml",
            root=("table", ["list-table"]),
            subelem_selectors=[
                SubelementSelector([], attribute="data-items")
            ],
            postprocess=lambda x: mal_json_parser(x[0][0])
        )
    )
)
