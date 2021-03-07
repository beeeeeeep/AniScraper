from torrent_client import TorrentClient, BinaryOperator
from config import DELUGE_HOST, DELUGE_PORT


torrent = TorrentClient(
    command_name="deluge-console",
    flags=["-d", DELUGE_HOST, "-p", DELUGE_PORT],
    operators={
        "add": BinaryOperator("add", arg1_flag="-p")
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)