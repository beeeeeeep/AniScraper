import unittest
from typing import Dict
from unittest.mock import patch, mock_open
from main import start
from implementations.anime_list.mal import ptw
from implementations.indexer.nyaa import indexer
import yaml


def load_test_config() -> Dict:
    return {
        'media': {
            'series': '/disk/media/series',
            'films': '/disk/media/films',
            'torrents': '/disk/torrents'
        },
        'docker': {
            'openvpn_profile_path': '',
            'docker_user': 1000,
            'docker_group': 1000
        },
        'preferences': {
            'account': 'aniscraper_test',
            'disable_new_anime': False,
            'min_series_size': 2,
            'min_movie_size': 1,
            'prefer_bluray': True,
            'quality': '1080p',
            'groups': ['commie', 'erai-raws', 'horriblesubs', 'subsplease'],
            'min_seeders': 5,
            'interval': 600,
            'anime_list': 'mal',
            'indexer': 'nyaa',
            'torrent': 'rtorrent_xmlrpc'
        }
    }


class MainTest(unittest.TestCase):
    m = mock_open(read_data="testing")

    @patch("utils.files.open", m)
    @patch("main.load_config")
    @patch("main.os.path")
    @patch("service_classes.torrent_client.TorrentClient")
    def test_main(self, mock_torrent, mock_os_path, mock_load_config):
        start()
        # self.m.assert_called_once_with("./config.yml")
        mock_load_config.assert_called_once_with("./config.yml")
        mock_load_config.return_value = {"no": 1}
        # mock_os_path.isdir.assert_called_once_with()
        # mock_os_path.exists.assert_called_once_with("anime_ids.json")
        # mock_os_path.exists.return_value = False
        # self.m.assert_called_once_with("anime_list.json", "w")
        # handle = self.m()
        # handle.write.assert_called_once_with("{}")
        # mock_torrent.execute.assert_called_once_with("add", "lmao", "yeet")
