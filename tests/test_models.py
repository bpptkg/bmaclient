import unittest

from bmaclient.models import DataModel


class DataModelTest(unittest.TestCase):
    def test_empty_keys(self):
        model = DataModel()
        self.assertCountEqual(model.get_keys(), list())
        self.assertDictEqual(model.as_dict(), dict())

    def test_setter(self):
        model = DataModel()
        model["key1"] = "value1"
        model["key2"] = "value2"
        self.assertCountEqual(model.get_keys(), ["key1", "key2"])
        self.assertDictEqual(model.as_dict(), {"key1": "value1", "key2": "value2"})

    def test_getter(self):
        model = DataModel()
        model["key1"] = "value1"
        model["key2"] = "value2"
        self.assertEqual(model["key1"], "value1")
        self.assertEqual(model["key2"], "value2")

    def test_object_from_dict(self):
        dict_data = {"key1": "value1", "key2": "value2"}
        model = DataModel(**dict_data)
        self.assertCountEqual(model.get_keys(), ["key1", "key2"])
        self.assertDictEqual(model.as_dict(), {"key1": "value1", "key2": "value2"})


if __name__ == "__main__":
    unittest.main()
