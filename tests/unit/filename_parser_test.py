import unittest
import json
from utils.filename_parser import parse_filename


class FilenameParserTest(unittest.TestCase):
    def test_data(self):
        with open("../tests/data/filename_parser_test.json") as fp:
            data = json.load(fp)
        for k, v in data.items():
            parse = parse_filename(k)
            for attr_name, attr_val in v.items():
                self.assertEqual(getattr(parse, attr_name), attr_val, attr_name)


if __name__ == '__main__':
    unittest.main()
