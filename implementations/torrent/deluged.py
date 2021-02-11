from torrent_client import TorrentClient, BinaryOperator


torrent = TorrentClient(
    command_name="deluge-console", 
    operators={
        "add": BinaryOperator("add", arg1_flag="-p")
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)