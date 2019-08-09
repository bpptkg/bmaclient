import os
import unittest

from bmaclient.bind import APIError
from bmaclient.client import MonitoringAPI
from bmaclient.utils import get_api_key, get_access_token


class SlopeAPITestWithAPIKey(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(api_key=get_api_key())

    def test_permissions(self):
        api = MonitoringAPI()
        self.assertRaises(APIError, api.fetch_slope)

    def test_fetch_slope(self):
        response = self.api.fetch_slope()
        self.assertIsNotNone(response)

    def test_search_slope(self):
        response = self.api.search_slope(search='RB2')
        self.assertIsNotNone(response)


class SlopeAPITestWithAccessToken(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(access_token=get_access_token())
        self.pk = None

    def step1_permissions(self):
        api = MonitoringAPI()
        self.assertRaises(APIError, api.fetch_slope)

    def step2_create_slope(self):
        data = {
            'timestamp': '2019-01-01 09:46:00',
            'deviation': 0.013,
            'benchmark': 'BAB0',
            'reflector': 'RB2',
        }
        response = self.api.create_slope(**data)
        self.assertIsNotNone(response)
        self.pk = response['id']

    def step3_fetch_slope(self):
        response = self.api.fetch_slope()
        self.assertIsNotNone(response)

    def step4_replace_slope(self):
        data = {
            'pk': self.pk,
            'timestamp': '2019-02-02 09:46:00',
            'deviation': 0.03,
            'benchmark': 'KAL0',
            'reflector': 'RK2',
        }
        response = self.api.replace_slope(**data)
        self.assertIsNotNone(response)

    def step5_update_slope(self):
        data = {
            'pk': self.pk,
            'reflector': 'RK3',
        }
        response = self.api.update_slope(**data)
        self.assertIsNotNone(response)

    def step6_search_slope(self):
        response = self.api.search_slope(search='RB1')
        self.assertIsNotNone(response)

    def step7_delete_slope(self):
        response = self.api.delete_slope(pk=self.pk)
        self.assertIsNone(response)

    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail('{} failed ({}: {})'.format(step, type(e), e))


if __name__ == '__main__':
    unittest.main()
