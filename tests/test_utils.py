import os
import unittest

from bmaclient import utils
from bmaclient.models import DataModel


class UtilTest(unittest.TestCase):
    def test_encode_string(self):
        self.assertEqual(utils.encode_string("test string"), b"test string")

    def test_object_from_list(self):
        entry = [{"key1": "value1"}, {"key2": "value2"}]
        model = utils.object_from_list(entry)

        self.assertEqual(model[0]["key1"], "value1")
        self.assertEqual(model[1]["key2"], "value2")

        for item in model:
            self.assertTrue(isinstance(item, DataModel))

    def test_get_api_key(self):
        os.environ["API_KEY"] = "TEST_API_KEY"
        self.assertEqual(utils.get_api_key(), "TEST_API_KEY")

    def test_get_access_token(self):
        os.environ["ACCESS_TOKEN"] = "TEST_ACCESS_TOKEN"
        self.assertEqual(utils.get_access_token(), "TEST_ACCESS_TOKEN")

    def test_encode_parameters(self):
        params = {
            "key1": 1,
            "key2": 2,
            "key3": "3",
            "key4": b"4",
        }
        self.assertDictEqual(
            utils.encode_parameters(params),
            {"key1": b"1", "key2": b"2", "key3": b"3", "key4": b"4"},
        )


if __name__ == "__main__":
    unittest.main()
