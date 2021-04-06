import unittest

from implementations.indexer.nyaa import indexer
from service_classes.indexer import Indexer
from tests.data.indexer_test_data import tests


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
        for i, item in enumerate(tests):
            with self.subTest(item["name"], i=i):
                if not item["enable"]:
                    continue
                indexer_results = item["data"].keys()
                rank = Indexer.rank(indexer_results, **item["rank_settings"], return_ranks=True)
                correct_ranks = {x.title: y for x, y in item["data"].items() if y is not None}
                correct_ranks = dict(sorted(correct_ranks.items(), key=lambda x: x[1]))
                correct_items = [x for x, y in item["data"].items() if y is not None]
                diff_table_list = [("Correct" + " " * 43, "Actual")] + [(x[:50], y[0].title[:50] + " " + str(y[1])) for x, y
                                                                        in zip(correct_ranks.keys(), rank)]
                difference_table = "\n".join([f"{x}          {y}" for x, y in diff_table_list])
                self.assertEqual(len(rank), len(correct_items),
                                 f"Ranked results had length {len(rank)}, expected {len(correct_items)}\n"
                                 f"Expected: {[x.title[:25] for x in correct_items]}\n"
                                 f"Was: {[x[0].title[:25] for x in rank]}")
                last_highest = 0
                for rankedResult, num_rank in rank:
                    correct_rank = correct_ranks.get(rankedResult.title)
                    if correct_rank == last_highest + 1:
                        last_highest += 1
                    self.assertEqual(last_highest, correct_ranks.get(rankedResult.title),
                                     f"Expected {rankedResult.title} to be rank {correct_ranks.get(rankedResult.title)}, was {last_highest}\n\nDifference table:\n{difference_table}")


if __name__ == '__main__':
    unittest.main()
