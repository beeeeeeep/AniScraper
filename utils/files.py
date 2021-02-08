import json
import os
import time
from scraper import Search


def prepare_dir(directory: str, search: Search) -> None:
    with open("anime_ids.json") as fp:
        anime_ids = json.load(fp)
    if anime_ids.get(directory) is None:
        anime_ids[directory] = {}
    if not directory.endswith("/"):
        directory = directory + "/"
    for file in os.listdir(directory):
        if file in anime_ids[directory]:
            continue
        anime_id = search.search(file)
        anime_ids[directory][file] = anime_id
        print(f"Found MAL ID for {file} - {anime_id}")
        time.sleep(5)
    with open("anime_ids.json", "w") as fp:
        json.dump(anime_ids, fp, indent=4)