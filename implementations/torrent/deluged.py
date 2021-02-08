from torrent_client import TorrentClient, BinaryOperator


deluged = TorrentClient(
    command_name="deluge-console", 
    operators={
        "add": BinaryOperator("add")
    }
)