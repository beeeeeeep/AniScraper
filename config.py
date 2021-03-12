MEDIA_DIR_SERIES = "/disk/media/series"  # series are symlinked into this dir
MEDIA_DIR_FILMS = "/disk/media/anime_films"  # films are symlinked into this dir
TORRENT_DIR = "/disk/torrents"  # torrent files are stored here
OPENVPN_PROFILE_PATH = ""  # ovpn profile file

DISABLE_NEW_ANIME = False  # disables downloading of anime newer than 2020, as these sometimes have unreliable batches.
ACCOUNT = ""  # anime list account
MIN_SERIES_SIZE = 2  # the minimum accepted size of TV shows in GiB
INDEXER_KEYWORDS = ["blu-ray", "blu ray", "(bd", "[bd", "bdrip"]  # results containing these in the title are more likely to be chosen
INDEXER_QUALITY = "1080p"  # preferred quality. Not a hard limit.
INDEXER_GROUPS = ["commie", "erai-raws", "horriblesubs", "subsplease"]  # preferred release groups

INTERVAL = 10 * 60  # interval between ptw list fetches in seconds

TORRENT_HOST = "localhost"
TORRENT_PORT = "5030"

# User which owns the MEDIA directories. Find using "id" command.
DOCKER_USER = "1000"
DOCKER_GROUP = "1000"

# Selects which implementations to use
ANIME_LIST = "mal"
INDEXER = "nyaa"
TORRENT = "rtorrent_xmlrpc"

# Don't change
MEDIA_DIR_SERIES_INTERNAL = "/series/"  
MEDIA_DIR_FILMS_INTERNAL = "/films/"  
TORRENT_DIR_INTERNAL = "/torrents/"
