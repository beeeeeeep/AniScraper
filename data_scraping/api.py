from typing import Callable, List, Dict
import requests


class JSONSelector:

    def __init__(self, selection_path: List[str]):
        self.selection_path = selection_path

    def select(self, data: Dict):
        for key in self.selection_path:
            if isinstance(data, list) and key >= len(data):
                return None
            elif isinstance(data, dict) and data.get(key) is None:
                return None
            data = data[key]
        return data


class APIParser:

    def __init__(self, selectors: List[JSONSelector], headers: Dict = {}, postprocess: Callable = lambda x: x):
        self.headers = headers
        self.selectors = selectors
        self.__postprocess = postprocess

    def fetch(self, url: str, request_type: str, data: Dict[str, str]) -> List[str]:
        if request_type not in ["GET", "POST"]:
            raise ValueError(f"{request_type} is not a valid request type")
        if request_type == "GET":
            r = requests.get(url, data, headers=self.headers)
        else:
            r = requests.post(url, json=data, headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(f"Failed to fetch data: {r.status_code}")
        data = r.json()
        return self.__postprocess([x.select(data) for x in self.selectors])
