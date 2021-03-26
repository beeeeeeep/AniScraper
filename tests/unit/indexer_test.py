import unittest

from implementations.indexer.nyaa import indexer


class IndexerTests(unittest.TestCase):
    def test_search(self):
        mob = indexer.query("mob psycho")
        mob_titles = [x.title.strip() for x in mob]
        self.assertNotIn("Mob Psycho 100 - S1 + S2 (Batch, HEVC, Dual Audio, 1080p)", mob_titles)  # untrusted
        self.assertIn("[Judas] Mob Psycho 100 (Seasons 1-2 + OVA + Specials) [BD 1080p][HEVC x265 10bit][Dual-Audio]["
                      "Multi-Subs] (Batch)", mob_titles)
        judas = [x for x in mob if "[Judas]" in x.title][0]
        size, units = judas.size.split(" ")
        self.assertIn(units, ["GiB", "MiB", "KiB"])
        self.assertGreater(float(size), 0.0)

    def test_rank_seasons(self):
        one_punch = indexer.query("one punch man")
        opm_ranked = indexer.rank(one_punch, "One Punch Man", [], "1080p", [], "TV", 1)
        opm_titles = [x.title for x in opm_ranked]
        season2_matches = [x for x in opm_titles if any(y in x.lower() for y in ["s2", "season 2", "s02", "season 02"])]
        self.assertEqual(len(season2_matches), 0, season2_matches)


if __name__ == '__main__':
    unittest.main()
