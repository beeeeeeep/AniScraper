from service_classes.torrent_client import PythonFunctions, BinaryOperator
from utils.rtorrent_scgi import RTorrentSCGI


scgi = RTorrentSCGI("/config/.local/share/rtorrent/rtorrent.sock")

torrent = PythonFunctions(
    operators={
        "add": BinaryOperator(lambda x, y: scgi.request("load.start", "", x, f"d.directory.set={y}"))
    }
)

#xmlrpc localhost load.start "" .torrent-file d.directory_base.set="dir"
