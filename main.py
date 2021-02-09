from implementations.anime_list.mal import ptw, search
from utils.files import prepare_dir
from implementations.indexer.nyaa import nyaa
from implementations.torrent.deluged import deluged
from indexer import Indexer
from config import MEDIA_DIR_SERIES, MEDIA_DIR_FILMS, TORRENT_DIR, DISABLE_NEW_ANIME, MAL_ACCOUNT
import os
import json
import time
import re
import requests
from torrentool.torrent import Torrent


print("Preparing series directory")
prepare_dir(MEDIA_DIR_SERIES, search)
print("Preparing films directory")
prepare_dir(MEDIA_DIR_FILMS, search)

with open("anime_ids.json") as fp:
    anime_ids = json.load(fp)
    series = anime_ids[MEDIA_DIR_SERIES]
    films = anime_ids[MEDIA_DIR_FILMS]

scrape = ptw.scrape(f"https://myanimelist.net/animelist/{MAL_ACCOUNT}?status=6")
for anime in scrape:
    anime_title = re.sub(r"[^0-9a-zA-Z\ \-\&]+", " ", anime[0])
    anime_id = str(anime[1])
    anime_type = anime[2]
    anime_year = int(anime[3]["year"])

    if anime_type == "Movie" and anime_id in films.values():
        continue
    elif anime_id in series.values():
        continue

    if anime_year >= 2020 and DISABLE_NEW_ANIME:
        print(f"WARNING: {anime_title} is newer than 2020. Please add manually on Sonarr.")
        continue
        
    query = nyaa.query(anime_title)
    if len(query) == 0:
        error_msg = f"WARNING: could not find anime with title {anime_title} on indexer nyaa"
        print(error_msg)
        continue
    data = [{"title": x[0], "link": "https://nyaa.si" + x[1], "seeders": x[2], "size": x[3]} for x in query]
    top_ranks = Indexer.rank(
        data, 
        pref_groups=["commie", "erai-raws", "horriblesubs", "subsplease"], 
        pref_quality="1080p", 
        keywords=["blu-ray", "blu ray", "(bd", "[bd", "bdrip"],
        type=anime_type,
        min_gib=2 if anime_type == "TV" else None,  #TODO: this is quite jank, fix
        prefer_first_season=True
    )

    if len(top_ranks) == 0:
        error_msg = f"WARNING: Could not find a suitable batch on nyaa for {anime_title}"
        if anime_year > 2018:
            error_msg += ". This anime aired in 2019 or later, so it is possible it doesn't yet have batches. Try adding it on Sonarr."
        print(error_msg)
        continue

    torrent_url = top_ranks[0]["link"]
    r = requests.get(torrent_url)
    if r.status_code != 200:
        raise ConnectionError("Failed to fetch torrent file")
    torrent_file_name = Torrent.from_string(r.content).name
    success = deluged.execute("add", ("-p", TORRENT_DIR), (None, torrent_url))
    if not success:
        raise RuntimeError("Torrent client error")
    if anime_type == "Movie":
        new_file_dir = MEDIA_DIR_FILMS
        films[anime_title] = anime_id
    else:
        new_file_dir = MEDIA_DIR_SERIES
        series[anime_title] = anime_id
    os.mkdir(new_file_dir + anime_title)
    if any(torrent_file_name.endswith(x) for x in [".mp4", ".mkv"]):
        new_filepath = "/" + torrent_file_name
    else:
        new_filepath = "/Season 1"
    os.symlink(TORRENT_DIR + torrent_file_name, new_file_dir + anime_title + new_filepath)
    print(f"Added ({anime_type}) {anime_title}")

    with open("anime_ids.json", "w") as fp:
        json.dump(anime_ids, fp, indent=4)
