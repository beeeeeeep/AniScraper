from utils.files import prepare_dir
from implementations.anime_list.mal import ptw
from implementations.search.anilist import search
from implementations.indexer.nyaa import indexer
from implementations.torrent.deluged import deluged
from indexer import Indexer
from config import INDEXER_GROUPS, MEDIA_DIR_SERIES, MEDIA_DIR_FILMS, TORRENT_DIR, DISABLE_NEW_ANIME, ACCOUNT, MIN_SERIES_SIZE, INDEXER_KEYWORDS, INDEXER_QUALITY
import os
import json
import time
import re
import requests
from torrentool.torrent import Torrent


# Lookup IDs of already downloaded stuff
prepare_dir(MEDIA_DIR_FILMS, search)
prepare_dir(MEDIA_DIR_SERIES, search)

# Get IDs already in storage
with open("anime_ids.json") as fp:
    data = json.load(fp)
    series = data[MEDIA_DIR_SERIES]
    films = data[MEDIA_DIR_FILMS]
    blacklist = data.get("blacklist")  # To avoid repeating failing searches
    if blacklist is None:
        data["blacklist"] = []
        blacklist = data["blacklist"]

# Get plan to watch list
# format: List[Tuple[title, id, type, year]]
ptw_anime = ptw.fetch(ACCOUNT)

for anime in ptw_anime:
    anime_title = re.sub(r" +", " ", re.sub(r"[^0-9a-zA-Z\ \-\&]+", " ", anime[0])).strip()
    anime_id = str(anime[1])
    anime_type = anime[2]
    anime_year = int(anime[3])

    # Get anilist ID
    search_id = search.fetch(anime_title)
    if search_id is None:
        print(f"WARNING: ID search for {anime_title} returned None.")
        continue
    time.sleep(1)  # avoid anilist rate limit

    if search_id in blacklist:
        continue
    if anime_type == "Movie" and search_id in films.values():
        continue
    elif search_id in series.values():
        continue

    if anime_year >= 2020 and DISABLE_NEW_ANIME:
        print(f"INFO: {anime_title} is newer than 2020. Adding to blacklist.")
        blacklist.append(search_id)
        continue

    # Query the indexer
    indexer_query = indexer.query(anime_title)

    if len(indexer_query) == 0:
        error_msg = f"INFO: could not find anime with title {anime_title} on indexer. Adding to blacklist."
        print(error_msg)
        blacklist.append(search_id)
        continue
    top_ranks = Indexer.rank(
        indexer_query, 
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
        print(error_msg)
        continue

    torrent_url = top_ranks[0]["link"]

    # GET .torrent file, parse and get torrent file name
    r = requests.get(torrent_url)
    if r.status_code != 200:
        raise ConnectionError("Failed to fetch torrent file")
    torrent_file_name = Torrent.from_string(r.content).name

    # Add torrent using url
    success = deluged.execute("add", ("-p", TORRENT_DIR), (None, torrent_url))

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
    print(f"Added ({anime_type}) {anime_title}")

    with open("anime_ids.json", "w") as fp:
        json.dump(data, fp, indent=4)

# TODO: maybe unjank this 
with open("anime_ids.json", "w") as fp:
    json.dump(data, fp, indent=4)
