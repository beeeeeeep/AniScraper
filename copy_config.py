import re


with open("./config.py") as fp:
    data = fp.readlines()

data = [re.sub(r" ?= ?", "=", re.sub(r"\#.*$", "", x)) for x in data if any(y in x for y in ["MEDIA_DIR_SERIES", "MEDIA_DIR_FILMS", "TORRENT_DIR"])]
with open(".env", "w") as fp:
    fp.write("".join(data))
