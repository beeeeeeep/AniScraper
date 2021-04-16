import unittest

from implementations.anime_list.mal import ptw


class AnimeListTest(unittest.TestCase):
    def test_myanimelist(self):
        mal = ptw.fetch("aniscraper_test")
        self.assertEqual(len(mal), 3)
        animes = {
            "37999": ("Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", "TV"),
            "38000": ("Kimetsu no Yaiba", "TV"),
            "43299": ("Wonder Egg Priority", "TV")
        }
        found_ids = [x.anime_id for x in mal]
        for k, v in animes.items():
            self.assertIn(k, found_ids)
            found = [x for x in mal if x.anime_id == k][0]
            self.assertEqual(found.title, v[0])
            self.assertEqual(found.type, v[1], v[0])

    def test_nonexistant_account(self):
        try:
            ptw.fetch("thisaccountdoesnotexistdsjkfhkjashdfkjashdfkjashkfdjhakjsdfh")
        except ConnectionError:
            pass


if __name__ == '__main__':
    unittest.main()
