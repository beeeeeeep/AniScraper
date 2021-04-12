import unittest
from typing import Dict
from unittest.mock import patch, mock_open

from implementations.anime_list.mal import ptw
from implementations.indexer.nyaa import indexer
from main import run_check


def load_test_config() -> Dict:
    return {
        'media': {
            'series': '/series/',
            'films': '/films/',
            'torrents': '/torrents/'
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
    @patch("main.store_anime_ids")
    @patch("main.os.symlink")
    @patch("main.os.mkdir")
    @patch("main.load_anime_ids")
    @patch("service_classes.torrent_client.TorrentClient")
    def test_main(self, mock_torrent, mock_load_anime_ids, mock_mkdir, mock_symlink, mock_store_anime_ids):
        config = load_test_config()
        mock_load_anime_ids.return_value = {
            "downloaded": [],
            "blacklist": []
        }
        run_check(ptw, indexer, mock_torrent, config["media"], config["preferences"])
        mock_load_anime_ids.assert_called_once_with("anime_ids.json")
        mock_torrent.execute.assert_called_once_with("add", "https://nyaa.si/download/1365504.torrent",
                                                     config["media"]["torrents"])
        mock_mkdir.assert_called_once_with(config["media"]["series"] + "Wonder Egg Priority")
        mock_symlink.assert_called_once_with(
            config["media"]["torrents"] + "[Nyanpasu] Wonder Egg Priority 1-12 Batch [1080p][HEVC]",
            config["media"]["series"] + "Wonder Egg Priority/Season 1"
        )
        mock_store_anime_ids.assert_called_once_with("./anime_ids.json", {
            "downloaded": [124845],
            "blacklist": []
        })
