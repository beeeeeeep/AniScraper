from torrent_client import PythonFunctions, ShellProgram, BinaryOperator
from config import TORRENT_HOST, TORRENT_PORT
from scgi.rtorrent_scgi import RTorrentSCGI


scgi = RTorrentSCGI("/config/.local/share/rtorrent/rtorrent.sock")

torrent = PythonFunctions(
    operators={"add": lambda x, y: scgi.request("load.start", "", x, f"d.directory.set={y}")}
)

#xmlrpc localhost load.start "" .torrent-file d.directory_base.set="dir"
