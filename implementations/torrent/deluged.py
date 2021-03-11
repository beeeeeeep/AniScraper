from torrent_client import ShellProgram, BinaryOperator
from config import TORRENT_HOST, TORRENT_PORT


torrent = ShellProgram(
    command_name="deluge-console",
    params=[],
    operators={
        "add": BinaryOperator(lambda arg1, arg2: ["add", arg1, "-p", arg2])
    },
    error_strings=["Torrent was not added"],
    success_strings=["Torrent added!"]
)
