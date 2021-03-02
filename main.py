from torrent_client import TorrentClient
from utils.files import prepare_dir
from implementations.search.anilist import search
from indexer import Indexer
from config import ANIME_LIST, INDEXER, INDEXER_GROUPS, INTERVAL, MEDIA_DIR_SERIES, MEDIA_DIR_FILMS, TORRENT, TORRENT_DIR, DISABLE_NEW_ANIME, ACCOUNT, MIN_SERIES_SIZE, INDEXER_KEYWORDS, INDEXER_QUALITY
import os
import json
import time
import re
import requests
import sched
import logging
import importlib
from torrentool.torrent import Torrent
from animelist import AnimeList


anime_list_imp = importlib.import_module(f"implementations.anime_list.{ANIME_LIST}")
indexer_imp = importlib.import_module(f"implementations.indexer.{INDEXER}")
torrent_imp = importlib.import_module(f"implementations.torrent.{TORRENT}")

if not hasattr(anime_list_imp, "ptw") or not isinstance(anime_list_imp.ptw, AnimeList):
    raise RuntimeError("anime_list must define a variable \"ptw\" of type AnimeList")

if not hasattr(indexer_imp, "indexer") or not isinstance(indexer_imp.indexer, Indexer):
    raise RuntimeError("indexer must define a variable \"indexer\" of type Indexer")

if not hasattr(torrent_imp, "torrent") or not isinstance(torrent_imp.torrent, TorrentClient):
    raise RuntimeError("torrent must define a variable \"torrent\" of type TorrentClient")

ptw: AnimeList = anime_list_imp.ptw
indexer: Indexer = indexer_imp.indexer
torrent: TorrentClient = torrent_imp.torrent

s = sched.scheduler(time.time, time.sleep)

def once():
    logging.info("Running scrape")

    existing_files = os.listdir(MEDIA_DIR_SERIES) + os.listdir(MEDIA_DIR_FILMS)

    # Get IDs already in storage
    with open("anime_ids.json") as fp:
        data = json.load(fp)
        series = data[MEDIA_DIR_SERIES]
        films = data[MEDIA_DIR_FILMS]

    # Previously scraped anime IDs. This uses the PTW IDs to avoid waiting for anilist search IDs.
    with open("scraped.json") as fp:
        scraped = json.load(fp)

    # Get plan to watch list
    # format: List[Tuple[title, id, type, year]]
    ptw_anime = ptw.fetch(ACCOUNT)

    for anime in ptw_anime:
        anime_title = re.sub(r" +", " ", re.sub(r"[^0-9a-zA-Z\ \-\&]+", " ", anime.title)).strip()
        anime_id = anime.anime_id
        anime_type = anime.type
        anime_year = anime.year

        if anime_title in existing_files:
            continue

        if anime_id in scraped:
            continue

        scraped.append(anime_id)

        # Get anilist ID
        search_id = search.fetch(anime_title)
        if search_id is None:
            logging.warning(f"ID search for {anime_title} returned None.")
            continue
        time.sleep(1)  # avoid anilist rate limit

        if anime_type == "Movie" and search_id in films.values():
            continue
        elif search_id in series.values():
            continue

        if anime_year >= 2020 and DISABLE_NEW_ANIME:
            logging.info(f"{anime_title} is newer than 2020. Adding to blacklist.")
            continue

        # Query the indexer
        indexer_query = indexer.query(anime_title)

        if len(indexer_query) == 0:
            error_msg = f"could not find anime with title {anime_title} on indexer. Adding to blacklist."
            logging.info(error_msg)
            continue
        top_ranks = Indexer.rank(
            indexer_query,
            title=anime_title,
            pref_groups=INDEXER_GROUPS, 
            pref_quality=INDEXER_QUALITY, 
            keywords=INDEXER_KEYWORDS,
            type=anime_type,
            min_gib=MIN_SERIES_SIZE if anime_type == "TV" else None,  #TODO: this is quite jank, fix
            prefer_first_season=True
        )

        if len(top_ranks) == 0:
            error_msg = f"INFO: Could not find a suitable batch for {anime_title}."
            if anime_year > 2018:
                error_msg += "This anime aired in 2019 or later, so it is possible it doesn't yet have batches. Try adding it on Sonarr."
            logging.info(error_msg)
            continue

        torrent_url = top_ranks[0].link

        # GET .torrent file, parse and get torrent file name
        r = requests.get(torrent_url)
        if r.status_code != 200:
            raise ConnectionError("Failed to fetch torrent file")
        torrent_file_name = Torrent.from_string(r.content).name

        # Add torrent using url
        success = torrent.execute("add", TORRENT_DIR, torrent_url)

        if not success:
            raise RuntimeError("Torrent client error")
        if anime_type == "Movie":
            new_file_dir = MEDIA_DIR_FILMS
            films[anime_title] = search_id
        else:
            new_file_dir = MEDIA_DIR_SERIES
            series[anime_title] = search_id
        os.mkdir(new_file_dir + anime_title)
        if any(torrent_file_name.endswith(x) for x in [".mp4", ".mkv"]):
            new_filepath = "/" + torrent_file_name
        else:
            new_filepath = "/Season 1"
        os.symlink(TORRENT_DIR + torrent_file_name, new_file_dir + anime_title + new_filepath)
        logging.info(f"Added ({anime_type}) {anime_title}")

        with open("anime_ids.json", "w") as fp:
            json.dump(data, fp, indent=4)

    # TODO: maybe unjank this 
    with open("anime_ids.json", "w") as fp:
        json.dump(data, fp, indent=4)

    with open("scraped.json", "w") as fp:
        json.dump(scraped, fp, indent=4)

    logging.info("Scrape finished")

    s.enter(INTERVAL, 1, once)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

    # Lookup IDs of already downloaded stuff
    prepare_dir(MEDIA_DIR_FILMS, search)
    prepare_dir(MEDIA_DIR_SERIES, search)

    s.enter(0, 1, once)
    s.run()
