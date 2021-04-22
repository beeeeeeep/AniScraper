import re

from utils.files import load_config

config = load_config("./config.yml")

env_string = ""
for k, v in list(config["media"].items()) + list(config["docker"].items()):
    env_string += f"{k.upper()}={v}\n"

with open(".env", "w") as fp:
    fp.write(env_string)

with open(config["docker"]["openvpn_profile_path"]) as fp:
    ovpn = fp.read()

if "BEGIN CERTIFICATE" not in ovpn:
    exit(0)

start_match = re.escape("-----BEGIN CERTIFICATE-----")
end_match = re.escape("-----END CERTIFICATE-----")
with open("vpn-ca.crt", "w") as fp:
    fp.write(re.findall(rf"(?sm){start_match}.*{end_match}", ovpn)[0])
