import unittest

from implementations.anime_list.mal import ptw


class AnimeListTest(unittest.TestCase):
    def test_myanimelist(self):
        mal = ptw.fetch("ivs_eres")
        self.assertGreater(len(mal), 0)
        first = mal[0]
        self.assertIsInstance(first.anime_id, str)
        self.assertIsInstance(first.title, str)
        self.assertIsInstance(first.type, str)
        self.assertIsInstance(first.year, int)

    def test_nonexistant_account(self):
        try:
            ptw.fetch("thisaccountdoesnotexistdsjkfhkjashdfkjashdfkjashkfdjhakjsdfh")
        except ConnectionError:
            pass


if __name__ == '__main__':
    unittest.main()
