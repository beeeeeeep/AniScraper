import logging
import unittest
from typing import Dict
from unittest.mock import patch, mock_open, call

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
    CURRENT_ANIME = {
        17549: (
            "Non Non Biyori",
            "https://nyaa.si/download/1052306.torrent",
            "[Tsundere] Non Non Biyori [BDRip h264 1920x1080 10bit FLAC]",  # torrent title
            "[Tsundere] Non Non Biyori [BDRip h264 1920x1080 10bit FLAC]"  # torrent filename
        ),
        112641: (
            "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen",
            "https://nyaa.si/download/1355132.torrent",
            "[EMBER] Kaguya-sama: Love is War (2019-2020) (Season 1+2) [BDRip] [1080p Dual Audio HEVC 10 bits] (Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen)",
            "Kaguya-sama Love is War S01-S02 1080p Dual Audio BDRip 10 bits DD x265-EMBER"
        ),
        101922: (
            "Kimetsu no Yaiba",
            "https://nyaa.si/download/1311485.torrent",
            "[CBM] Demon Slayer: Kimetsu no Yaiba 1-26 Complete (Dual Audio) [BDRip 1080p x265 10bit]",
            "[CBM] Demon Slayer - Kimetsu no Yaiba 1-26 Complete (Dual Audio) [BDRip 1080p x265 10bit]"
        )
    }
    m = mock_open(read_data="testing")

    @patch("utils.files.open", m)
    @patch("main.store_anime_ids")
    @patch("main.os.symlink")
    @patch("main.os.mkdir")
    @patch("main.load_anime_ids")
    @patch("service_classes.torrent_client.TorrentClient")
    def test_main_once(self, mock_torrent, mock_load_anime_ids, mock_mkdir, mock_symlink, mock_store_anime_ids):
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(levelname)s] %(message)s",
                            datefmt="%d/%m/%Y %H:%M:%S")
        config = load_test_config()
        mock_torrent.execute.return_value = True
        mock_load_anime_ids.return_value = {
            "downloaded": [],
            "blacklist": []
        }
        run_check(ptw, indexer, mock_torrent, config["media"], config["preferences"])
        mock_load_anime_ids.assert_called_once_with("anime_ids.json")
        torrent_calls = [call("add", x[1], config["media"]["torrents"]) for x in self.CURRENT_ANIME.values()]
        mock_torrent.execute.assert_has_calls(torrent_calls, any_order=True)
        mkdir_calls = [call(config["media"]["series"] + x[0]) for x in self.CURRENT_ANIME.values()]
        mock_mkdir.assert_has_calls(mkdir_calls, any_order=True)
        symlink_calls = [call(config["media"]["torrents"] + x[3], config["media"]["series"] + x[0] + "/Season 1") for x in self.CURRENT_ANIME.values()]
        mock_symlink.assert_has_calls(symlink_calls, any_order=True)
        self.assertEqual(len(mock_store_anime_ids.mock_calls), 1)
