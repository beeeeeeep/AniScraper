from torrent_client import TorrentClient, BinaryOperator
from config import TORRENT_HOST, TORRENT_PORT


torrent = TorrentClient(
    command_name="xmlrpc",
    params=[f"{TORRENT_HOST}:{TORRENT_PORT}"],
    operators={
        "add": BinaryOperator(lambda arg1, arg2: [
            "load.start",
            "",
            arg1,
            f"d.directory_base.set={arg2}"
        ])
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)

#xmlrpc localhost load.start "" .torrent-file d.directory_base.set="dir"
