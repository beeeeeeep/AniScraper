import unittest
from unittest.mock import patch
from main import run_check


class MainTest(unittest.TestCase):

    @patch("service_classes.torrent_client.TorrentClient")
    def test_main(self, mock_torrent):
        run_check(mock_animelist, mock_indexer, mock_torrent)
        mock_os_path_exists.return_value = False
        mock_open.assert_called_once_with("anime_list.json", "w")
        # mock_torrent.execute.assert_called_once_with("add", "lmao", "yeet")
