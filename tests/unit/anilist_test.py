import unittest

from implementations.search.anilist import search


class AniListSearchTest(unittest.TestCase):
    def test_search(self):
        id_, year, romaji, english = search.fetch("jojo")
        self.assertEqual(id_, 14719)
        self.assertEqual(year, 2012)
        self.assertEqual(romaji, "JoJo no Kimyou na Bouken")
        self.assertEqual(english, "JoJo's Bizarre Adventure")

if __name__ == '__main__':
    unittest.main()
