import os
import unittest

from bmaclient.bind import APIError
from bmaclient.client import MonitoringAPI
from bmaclient.utils import get_api_key, get_access_token


class UsersAPITestWithAPIKey(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(api_key=get_api_key())

    def test_permissions(self):
        api = MonitoringAPI()
        self.assertRaises(APIError, api.fetch_users)

    def test_fetch_users(self):
        response = self.api.fetch_users()
        self.assertIsNotNone(response)

    def test_user(self):
        response = self.api.user(pk=1)
        self.assertIsNotNone(response)

    def test_search_users(self):
        response = self.api.search_users(search='iori')
        self.assertIsNotNone(response)


class UsersAPITestWithAccessToken(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(access_token=get_access_token())

    def test_permissions(self):
        api = MonitoringAPI()
        self.assertRaises(APIError, api.fetch_users)

    def test_fetch_users(self):
        response = self.api.fetch_users()
        self.assertIsNotNone(response)

    def test_user(self):
        response = self.api.user(pk=1)
        self.assertIsNotNone(response)

    def test_search_users(self):
        response = self.api.search_users(search='indra')
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
