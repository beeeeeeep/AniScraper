from indexer import Indexer
from scraper import Scraper, SubelementSelector


nyaa = Indexer(
    url="https://nyaa.si/",
    fields_format=lambda x: f"?f=1&c=1_2&q={x}&s=seeders&o=desc",
    scraper=Scraper(
        parser="lxml",
        root=["tr", ["success", "default"]],
        subelem_selectors=[
            SubelementSelector([("td", [], 1), ("a", [], -1)], attribute="text"),
            SubelementSelector([("td", ["text-center"], 0), ("a", [])], attribute="href"),
            SubelementSelector([("td", ["text-center"], 3)], attribute="text"),
            SubelementSelector([("td", ["text-center"], 1)], attribute="text")
        ]
    )
)