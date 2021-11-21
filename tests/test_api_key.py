import os
import unittest

from bmaclient.utils import get_api_key_from_file

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class APIKeyTest(unittest.TestCase):
    def test_get_api_key_from_file(self):
        path = os.path.join(DATA_DIR, "api_key.txt")
        key = get_api_key_from_file(path)
        self.assertEqual(key, "THIS_IS_API_KEY_VALUE")

    def test_get_api_key_from_empty_file(self):
        path = os.path.join(DATA_DIR, "api_key_empty.txt")
        key = get_api_key_from_file(path)
        self.assertEqual(key, "")

    def test_get_api_key_from_empty_file_strict(self):
        path = os.path.join(DATA_DIR, "api_key_empty.txt")
        with self.assertRaises(ValueError):
            key = get_api_key_from_file(path, strict=True)


if __name__ == "__main__":
    unittest.main()
