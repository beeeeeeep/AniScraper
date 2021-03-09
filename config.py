MEDIA_DIR_SERIES = "/series"  # series are symlinked into this dir
MEDIA_DIR_FILMS = "/films"  # films are symlinked into this dir
TORRENT_DIR = "/torrents/"  # torrent files are stored here

DISABLE_NEW_ANIME = False  # disables downloading of anime newer than 2020, as these sometimes have unreliable batches.
ACCOUNT = ""  # anime list account
MIN_SERIES_SIZE = 2  # the minimum accepted size of TV shows in GiB
INDEXER_KEYWORDS = ["blu-ray", "blu ray", "(bd", "[bd", "bdrip"]  # results containing these in the title are more likely to be chosen
INDEXER_QUALITY = "1080p"  # preferred quality. Not a hard limit.
INDEXER_GROUPS = ["commie", "erai-raws", "horriblesubs", "subsplease"]  # preferred release groups

INTERVAL = 10 * 60  # interval between ptw list fetches in seconds

TORRENT_HOST = "localhost"
TORRENT_PORT = "5030"

# Selects which implementations to use
ANIME_LIST = "mal"
INDEXER = "nyaa"
TORRENT = "deluged"
