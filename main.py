import importlib
import json
import logging
import os
import sched
import time
from argparse import ArgumentParser
from datetime import datetime

import requests
from torrentool.torrent import Torrent

from config import ANIME_LIST, INDEXER, INDEXER_GROUPS, INTERVAL, MEDIA_DIR_SERIES_INTERNAL, MEDIA_DIR_FILMS_INTERNAL, \
    TORRENT, TORRENT_DIR, TORRENT_DIR_INTERNAL, DISABLE_NEW_ANIME, ACCOUNT, MIN_SERIES_SIZE, INDEXER_PREFER_BD, \
    INDEXER_QUALITY, MIN_MOVIE_SIZE, MIN_SEEDERS
from implementations.search.anilist import search
from service_classes.animelist import AnimeList
from service_classes.indexer import Indexer
from service_classes.torrent_client import ShellProgram
from utils.files import setup_dir, load_anime_ids, store_anime_ids

anime_list_imp = importlib.import_module(f"implementations.anime_list.{ANIME_LIST}")
indexer_imp = importlib.import_module(f"implementations.indexer.{INDEXER}")
torrent_imp = importlib.import_module(f"implementations.torrent.{TORRENT}")

if not hasattr(anime_list_imp, "ptw") or not isinstance(anime_list_imp.ptw, AnimeList):
    raise RuntimeError("anime_list must define a variable \"ptw\" of type AnimeList")

if not hasattr(indexer_imp, "indexer") or not isinstance(indexer_imp.indexer, Indexer):
    raise RuntimeError("indexer must define a variable \"indexer\" of type Indexer")

if not hasattr(torrent_imp, "torrent"):
    raise RuntimeError("torrent must define a variable \"torrent\" of type TorrentClient")

ptw: AnimeList = anime_list_imp.ptw
indexer: Indexer = indexer_imp.indexer
torrent: ShellProgram = torrent_imp.torrent

s = sched.scheduler(time.time, time.sleep)


def get_torrent_name(torrent_url):
    r = requests.get(torrent_url)
    if r.status_code != 200:
        raise ConnectionError("Failed to fetch torrent file")
    return Torrent.from_string(r.content).name


def run_check():
    logging.info("Running scrape")

    # Get IDs in storage
    anime_ids = load_anime_ids("anime_ids.json")

    # Get plan to watch list
    try:
        ptw_anime = ptw.fetch(ACCOUNT)
    except ConnectionError:
        logging.warning("Failed to connect to anime list service")
        return

    for anime in ptw_anime:
        anime_title = anime.title
        anime_year = anime.year

        # Get AniList ID
        anilist_id, anilist_title = search.fetch(anime_title)
        if anilist_id is None:
            logging.warning(f"No AniList results for {anime_title}. Ignoring.")
            continue

        if anime_year >= datetime.now().year - 1 and DISABLE_NEW_ANIME:
            logging.info(f"{anime_title} is newer than 2020. Ignoring.")
            continue

        # Query the indexer
        indexer_query = indexer.query(anime_title)

        if len(indexer_query) == 0:
            logging.info(f"Could not find anime with title {anime_title} on indexer. Ignoring.")
            continue
        top_ranks = Indexer.rank(
            indexer_query,
            title=anilist_title,
            pref_groups=INDEXER_GROUPS,
            pref_quality=INDEXER_QUALITY,
            season=1,
            min_gib=MIN_MOVIE_SIZE if anime.anime_type == "Movie" else MIN_SERIES_SIZE,
            min_seeders=MIN_SEEDERS,
            seeders_importance=0.5  # TODO: find best
        )

        if len(top_ranks) == 0:
            error_msg = f"INFO: Could not find a suitable batch for {anime_title}. "
            recent = datetime.now().year - 3
            if anime_year > recent:
                error_msg += f"This anime aired later than {recent}, so it may not have batches yet. Try adding it on Sonarr."
            logging.info(error_msg)
            continue

        torrent_url = top_ranks[0].link

        # GET .torrent file, parse and get torrent file name
        torrent_file_name = get_torrent_name(torrent_url)

        # Add torrent using url
        success = torrent.execute("add", torrent_url, TORRENT_DIR_INTERNAL)

        if not success:
            raise RuntimeError("Torrent client error")
        if anime.type == "Movie":
            media_dir = MEDIA_DIR_FILMS_INTERNAL
        else:
            media_dir = MEDIA_DIR_SERIES_INTERNAL
        if not media_dir.endswith("/"):
            media_dir += "/"
        os.mkdir(media_dir + anime_title)
        os.symlink(TORRENT_DIR + torrent_file_name, media_dir + anime_title + "/Season 1" if anime.type == "TV" else "")
        anime_ids["downloaded"].append(anilist_id)
        logging.info(f"Added ({anime.type}) {anilist_title}")

        time.sleep(1)  # comply with anilist rate limit

    store_anime_ids("./anime_ids.json", anime_ids)
    logging.info("Scrape finished")


def run_once():
    run_check()
    s.enter(INTERVAL, 1, run_once)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s",
                        datefmt="%d/%m/%Y %H:%M:%S")

    parser = ArgumentParser(description="An anime torrent automation tool.")

    if ACCOUNT == "":
        exit("Account setting cannot be empty. Check config.py")

    if not os.path.exists("anime_ids.json"):
        with open("anime_ids.json", "w") as fp:
            fp.write("{}")

    # Lookup IDs of already downloaded stuff
    setup_dir(MEDIA_DIR_FILMS_INTERNAL, search)
    setup_dir(MEDIA_DIR_SERIES_INTERNAL, search)

    s.enter(0, 1, run_once)
    s.run()
