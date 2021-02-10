# AniScraper
AniScraper is an anime plan-to-watch list torrent automation tool, designed to be extensible to support any combination of PTW list, indexer and torrent client.

The current version is by default configured with MyAnimeList, nyaa.si and deluge-console.

This software is in very early development stages, so there are many bugs right now.

## Installation
Clone the repository, then run
```
pip install -r requirements.txt
```
`config.py` contains various settings, including media filepaths and PTW list account. Edit these before starting.

Launch with
```
python main.py
```

This will look up each show/film on your PTW on an indexer, order the results based on number of seeders, quality, season, and add the most suitable torrent to your client.

## Extensibility
This tool offers extensibility to allow use of other PTW lists, indexers and torrent clients. Implementations of these are declared in `implementations`. It is currently not recommended to add to the current set, more will be coming in the future.

More updates soon.