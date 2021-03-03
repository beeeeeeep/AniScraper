# AniScraper
AniScraper is an anime plan-to-watch list torrent automation tool, designed to be extensible to support any combination of PTW list, indexer and torrent client.

The current version is by default configured with MyAnimeList, nyaa.si and deluge-console.

This software is in very early development stages, so there are many bugs right now.

## Requirements

- Python 3.8 and pip.
- The default configuration requires a [MAL](https://myanimelist.net) account and [deluge-console](https://dev.deluge-torrent.org/wiki/UserGuide/ThinClient).

## Configuration

`config.py` contains parameters to control file, indexing and other configuration preferences.

## Installation
```
git clone https://github.com/beeeeeeep/AniScraper
pip install -r requirements.txt
```

Launch with
```
python main.py
```
This runs a loop which fetches the PTW list every 10 minutes by default.

## Extensibility
This tool offers extensibility to allow use of other PTW lists, indexers and torrent clients. Implementations of these are declared in `implementations`. Which implementation is used is defined in `config.py` - this should be set as a string containing name of the python module. If you would like to extend these yourself, read on.

Anime lists and indexers make use of `DataSource`s (`WebScrapeSource` or `APISource`), which define rules for fetching data for a query. See examples below. (More docs for this coming soon).

### Plan-to-watch service `(implementations.anime_list)`

Expects a variable `ptw` of type `AnimeList` to be accessible. Example (myanimelist.net):

```python
def mal_json_parser(raw: str) -> str:
    data = json.loads(raw)
    return [
        (re.sub(r"\(TV\)|\(Movie\)|\(OVA\)", "", x["anime_title"], flags=re.IGNORECASE), 
        x["anime_id"], 
        x["anime_media_type_string"], 
        int(x["anime_season"]["year"])) for x in data]

ptw = AnimeList(
    WebScrapeSource(
        query_formatter=lambda x: f"https://myanimelist.net/animelist/{x}?status=6",
        scraper=Scraper(
            parser="lxml",
            root=["table", ["list-table"]],
            subelem_selectors=[
                SubelementSelector([], attribute="data-items")
            ],
            postprocess=lambda x: mal_json_parser(x[0][0])
        )
    )
)
```
This must be configured such that the scrape returns the title, anime ID (the one given by the PTW service), type (TV/Movie/OVA etc.) and year of showing in this order.

### Indexer `(implementations.indexer)`

Expects a variable `indexer` of type `Indexer` to be accessible. Example (nyaa.si):

```python
indexer = Indexer(
    WebScrapeSource(
        query_formatter=lambda x: f"https://nyaa.si/?f=1&c=1_2&q={x.replace(' ', '+')}&s=seeders&o=desc",
        scraper=Scraper(
            parser="lxml",
            root=["tr", ["success", "default"]],
            subelem_selectors=[
                SubelementSelector([("td", [], 1), ("a", [], -1)], attribute="text"),  # result title
                SubelementSelector([("td", ["text-center"], 0), ("a", [])], attribute="href"),  # (local) torrent link
                SubelementSelector([("td", ["text-center"], 3)], attribute="text"),  # seeders
                SubelementSelector([("td", ["text-center"], 1)], attribute="text")  # file size
            ],
            postprocess=lambda x: [(y[0], "https://nyaa.si/" + y[1], y[2], y[3]) for y in x]
        )
    )
)
```
The indexer expects result title, .torrent file link, number of seeders and size for each matching result to be returned, in this order. These are then used to rank the results according to seeders, season, filesize etc.

### Torrent Client `(implementations.torrent)`

Expects a variable `torrent` of type `TorrentClient` to be accessible. Example (deluged):
```python
torrent = TorrentClient(
    command_name="deluge-console", 
    operators={
        "add": BinaryOperator("add", arg1_flag="-p")
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)
```
This runs the defined commands in shell. Only the "add" command is necessary right now. 

### Search `(implementations.search)`

This is only used for internal ID purposes, so it is not recommended to modify this. AniList IDs are used.
