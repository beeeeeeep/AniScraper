import re

from implementations.indexer.nyaa import indexer
from service_classes.indexer import Indexer


def gen_indexer_test_data(search: str, indexer: Indexer) -> str:
    """Generate an indexer test data string based on a specific indexer search"""
    results = indexer.query(search)
    unique_results = []
    for result in results:
        if re.sub(r"[0-9A-F]*", "", result.title) in [re.sub(r"[0-9A-F]*", "", x.title) for x in unique_results]:
            continue
        unique_results.append(result)
    indexer_results = ",\n        ".join([f'IndexerResult("{x.title}", "", {x.seeders}, "{x.size}"): None' for x in unique_results])
    return f"""{{
    "enable": True,
    "data": {{
        {indexer_results}
    }},
    "rank_settings": {{"title": "{results[0].title}", "pref_groups": ["HorribleSubs", "Erai-raws"],
                      "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 1}}
}},
"""


print(gen_indexer_test_data("mononoke", indexer))
