import re
from config import OPENVPN_PROFILE_PATH


with open("./config.py") as fp:
    data = fp.readlines()

data = [re.sub(r" ?= ?", "=", re.sub(r"\#.*$", "", x)) for x in data if any(x.split("=")[0].strip() == y for y in ["MEDIA_DIR_SERIES", "MEDIA_DIR_FILMS", "TORRENT_DIR", "OPENVPN_PROFILE_PATH"])]
with open(".env", "w") as fp:
    fp.write("".join(data))

with open(OPENVPN_PROFILE_PATH) as fp:
    ovpn = fp.read()

if "BEGIN CERTIFICATE" not in ovpn:
    exit(0)

start_match = re.escape("-----BEGIN CERTIFICATE-----")
end_match = re.escape("-----END CERTIFICATE-----")
with open("vpn-ca.crt", "w") as fp:
    fp.write(re.findall(rf"(?sm){start_match}.*{end_match}", ovpn)[0])
