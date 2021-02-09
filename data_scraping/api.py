from typing import List, Dict
import requests


class JSONSelector:

    def __init__(self, selection_path: List[str]):
        self.selection_path = selection_path

    def select(self, data: Dict):
        for key in self.selection_path:
            data = data[key]
        return data


class APIParser:

    def __init__(self, request_type: str, selectors: List[JSONSelector], headers: Dict = {}):
        self.headers = headers
        if request_type not in ["GET", "POST"]:
            raise ValueError(f"{request_type} is not a valid request type")
        self.request_type = request_type
        self.selectors = selectors

    def fetch(self, url: str, data: Dict[str, str]) -> List[str]:
        if self.request_type == "GET":
            r = requests.get(url, data, headers=self.headers)
        else:
            r = requests.post(url, json=data, headers=self.headers)
        data = r.json()
        return [x.select(data) for x in self.selectors]

query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search) {
            id
            title {
                romaji
            }
        }
    }
}
'''

pp = APIParser("POST", [JSONSelector(["data", "Page", "media", 0, "id"])])
pp.fetch("https://graphql.anilist.co", {
    "query": query,
    "variables": {
        "page": 1,
        "search": "test",
        "sort": "SEARCH_MATCH",
        "type": "ANIME"
    }
})
