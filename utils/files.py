import json
import os
import time
from typing import Dict

from service_classes.search import Search
import logging
import yaml


def setup_dir(directory: str, search: Search) -> None:
    logging.info(f"Preparing directory {directory}")
    if not os.path.isdir(directory):
        os.mkdir(directory)
        return
    with open("anime_ids.json") as fp:
        anime_ids = json.load(fp)
    if anime_ids.get(directory) is None:
        anime_ids[directory] = {}
    if not directory.endswith("/"):
        directory = directory + "/"
    for file in os.listdir(directory):
        if file in anime_ids[directory]:
            continue
        anime_id = search.fetch(file)
        if anime_id is not None:
            anime_ids[directory][file] = anime_id
            logging.info(f"Found ID for {file} - {anime_id}")
        else:
            logging.warning(f"Failed to find ID for {file}")
        time.sleep(2)
    with open("anime_ids.json", "w") as fp:
        json.dump(anime_ids, fp, indent=4)


def load_anime_ids(filename: str):
    if not os.path.exists("anime_ids.json"):
        with open("anime_ids.json", "w") as fp:
            fp.write("{}")
        return {"downloaded": [], "blacklist": []}
    with open(filename) as fp:
        anime_ids = json.load(fp)
        if anime_ids.get("downloaded") is None:
            anime_ids["downloaded"] = []
        if anime_ids.get("blacklist") is None:
            anime_ids["blacklist"] = []
    return anime_ids


def store_anime_ids(filename, ids):
    with open(filename, "w") as fp:
        json.dump(ids, fp)


def load_config(path: str) -> Dict:
    with open(path) as fp:
        data = yaml.safe_load(fp)
        for key in data["media"].keys():
            if not data["media"][key].endswith("/"):
                data["media"][key] += "/"
        return data
