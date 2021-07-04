import unittest

from bmaclient.client import MonitoringAPI
from bmaclient.exceptions import APIClientError


class FetchLavaDomesTest(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(api_key='TEST_API_KEY')

    def test_request_without_supplying_params(self):
        with self.assertRaises(APIClientError):
            self.api.fetch_lava_domes()

    def test_request_with_some_params(self):
        with self.assertRaises(APIClientError):
            self.api.fetch_lava_domes(location='BARAT DAYA')


class FetchRfapDistanceTest(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(api_key='TEST_API_KEY')

    def test_request_without_supplying_params(self):
        with self.assertRaises(APIClientError):
            self.api.fetch_rfap_distance()

    def test_request_with_some_params(self):
        with self.assertRaises(APIClientError):
            self.api.fetch_rfap_distance(start='2021-01-01')


if __name__ == '__main__':
    unittest.main()
