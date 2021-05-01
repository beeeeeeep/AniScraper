import importlib
import logging
import os
import re
import sched
import time
from argparse import ArgumentParser
from datetime import datetime
from typing import Dict, Callable

import requests
from torrentool.torrent import Torrent

from implementations.search.anilist import search
from service_classes.animelist import AnimeList
from service_classes.indexer import Indexer
from service_classes.torrent_client import TorrentClient
from utils.files import setup_dir, load_anime_ids, store_anime_ids, load_config

s = sched.scheduler(time.time, time.sleep)


def get_torrent_name(torrent_url):
    r = requests.get(torrent_url)
    if r.status_code != 200:
        raise ConnectionError("Failed to fetch torrent file")
    return Torrent.from_string(r.content).name


def run_check(ptw, indexer, torrent_client: TorrentClient, media_config: Dict, docker_config: Dict, preferences: Dict):
    logger.info("Running scrape")

    # Get IDs in storage
    anime_ids = load_anime_ids("anime_ids.json")

    # Get plan to watch list
    try:
        ptw_anime = ptw.fetch(preferences["account"])
    except ConnectionError:
        logger.error("Failed to connect to anime list service")
        return

    for anime in ptw_anime:
        anime_id = anime.anime_id
        anime_title = anime.title

        if anime_id in anime_ids["anilist_id_cache"]:
            anilist_id, a_year, a_title_romaji, a_title_english = anime_ids["anilist_id_cache"][anime_id]
        else:
            anilist_id, a_year, a_title_romaji, a_title_english = search.fetch(anime_title)
            anime_ids["anilist_id_cache"][anime_id] = [anilist_id, a_year, a_title_romaji, a_title_english]
            time.sleep(1)

        if anilist_id is None:
            logger.warning(f"No AniList results for {anime_title}. Ignoring.")
            continue

        if anilist_id in list(anime_ids["downloaded"].values()) + anime_ids["blacklist"]:
            continue

        if a_year >= datetime.now().year - 1 and preferences["disable_new_anime"]:
            logger.info(f"{anime_title} is newer than 2020. Ignoring.")
            continue

        # Query the indexer
        indexer_query = indexer.query(anime_title)

        if len(indexer_query) == 0:
            logger.info(f"Could not find anime with title {anime_title} on indexer. Ignoring.")
            continue
        top_ranks = Indexer.rank(
            indexer_query,
            anilist_id=anilist_id,
            titles=[a_title_romaji, a_title_english],
            pref_groups=preferences["groups"],
            pref_quality=preferences["quality"],
            season=1,
            min_gib=preferences["min_movie_size"] if anime.type == "Movie" else preferences["min_series_size"],
            min_seeders=preferences["min_seeders"],
            prefer_bluray=preferences["prefer_bluray"],
            seeders_importance=0.1  # TODO: find best
        )

        if len(top_ranks) == 0:
            error_msg = f"INFO: Could not find a suitable batch for {anime_title}. "
            recent = datetime.now().year - 3
            if a_year > recent:
                error_msg += f"This anime aired later than {recent}, so it may not have batches yet. Try adding it on Sonarr."
            logger.info(error_msg)
            continue

        torrent_url = top_ranks[0].link

        # GET .torrent file, parse and get torrent file name
        torrent_file_name = get_torrent_name(torrent_url)

        logger.debug(f"Torrent file: {torrent_file_name}")

        # Add torrent using url
        success = torrent_client.execute("add", torrent_url, media_config["torrents"])

        if not success:
            raise RuntimeError("Torrent client error")
        anime_title_clean = re.sub(r"[\\/*?:\"<>|]", "", anime_title)
        if anime.type == "Movie":
            media_dir = media_config["films"]
        else:
            media_dir = media_config["series"]
        if anime.type != "Movie":
            new_dir = media_dir + anime_title_clean
            if os.path.exists(new_dir):
                logger.warning(f"{new_dir} already exists, skipping")
                continue
            logger.debug(f"mkdir: {new_dir}")
            os.mkdir(new_dir)
        symlink_from = docker_config["docker_torrents"] + torrent_file_name
        symlink_to = media_dir + anime_title_clean + ("/Season 1" if anime.type != "Movie" else "")
        logger.debug(f"symlink: {symlink_from} -> {symlink_to}")
        os.symlink(symlink_from, symlink_to)
        anime_ids["downloaded"][anime_title] = anilist_id
        logger.info(f"Added ({anime.type}) {a_title_romaji}")

    store_anime_ids("./anime_ids.json", anime_ids)
    logger.info("Scrape finished")


def start():
    config = load_config("./config.yml")
    media_config = config["media"]
    docker_config = config["docker"]
    preferences = config["preferences"]

    ptw: AnimeList = importlib.import_module(f"implementations.anime_list.{preferences['anime_list']}").ptw
    indexer: Indexer = importlib.import_module(f"implementations.indexer.{preferences['indexer']}").indexer
    torrent: TorrentClient = importlib.import_module(f"implementations.torrent.{preferences['torrent']}").torrent

    if preferences['account'] == "":
        exit("Account setting cannot be empty. Check config.py")

    # Lookup IDs of already downloaded stuff
    setup_dir(media_config["films"], search)
    setup_dir(media_config["series"], search)

    schedule(run_check, preferences["interval"], ptw, indexer, torrent, media_config, docker_config, preferences)


def schedule(func: Callable, delay: int, *args):
    while True:
        func(*args)
        time.sleep(delay)


if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    parser = ArgumentParser(description="An anime torrent automation tool.")
    start()
