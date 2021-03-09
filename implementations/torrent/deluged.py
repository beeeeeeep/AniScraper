from torrent_client import TorrentClient, BinaryOperator
from config import TORRENT_HOST, TORRENT_PORT


torrent = TorrentClient(
    command_name="deluge-console",
    operators={
        "add": BinaryOperator(lambda arg1, arg2: ["add", arg1, "-p", arg2])
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)