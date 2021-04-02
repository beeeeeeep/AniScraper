import unittest

from implementations.indexer.nyaa import indexer
from service_classes.indexer import Indexer
from tests.data.indexer_test_data import data


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

    def test_rank(self):
        for item in data:
            indexer_results = item.keys()
            rank = Indexer.rank(indexer_results, "One Punch Man", ["HorribleSubs", "Erai-raws"], pref_quality="1080p",
                                season=1, min_gib=1)
            correct_ranks = {x.title: y for x, y in item.items()}
            expected_length = len([x for x in correct_ranks.values() if x is not None])
            diff_table_list = [("Correct" + " " * 43, "Actual")] + [(x[:50], y.title[:50]) for x, y in zip(correct_ranks.keys(), rank)]
            difference_table = "\n".join([f"{x}          {y}" for x, y in diff_table_list])
            self.assertEqual(len(rank), expected_length, f"Ranked results had length {len(rank)}, expected {expected_length}")
            for i, rankedResult in enumerate(rank):
                self.assertEqual(i, correct_ranks.get(rankedResult.title),
                                 f"Expected {rankedResult.title} to be rank {correct_ranks.get(rankedResult.title)}, was {i}\n\nDifference table:\n{difference_table}")


if __name__ == '__main__':
    unittest.main()
