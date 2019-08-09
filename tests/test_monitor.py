import os
import unittest

from bmaclient.bind import APIError
from bmaclient.client import MonitoringAPI
from bmaclient.utils import get_api_key, get_access_token

MONITORING_API = (
    'doas',
    'gas_emission',
    'edm',
    'gps_position',
    'gps_baseline',
    'rsam_seismic',
    'rsam_seismic_band',
    'rsam_infrasound',
    'rsam_infrasound_band',
    'thermal',
    'tiltmeter',
    'tiltmeter_raw',
    'tiltborehole',
    'seismicity',
    'bulletin',
    'energy',
    'magnitude',
)


class MonitoringAPITestWithAPIKey(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(api_key=get_api_key())

    def test_permissions(self):
        api = MonitoringAPI()
        for name in MONITORING_API:
            self.assertRaises(APIError, api.get_fetch_method(name))

    def test_fetch_method(self):
        for name in MONITORING_API:
            response = api.get_fetch_method(name)()
            self.assertIsNotNone(response)


class MonitoringAPITestWithAccessToken(unittest.TestCase):

    def setUp(self):
        self.api = MonitoringAPI(access_token=get_access_token())

    def test_permissions(self):
        api = MonitoringAPI()
        for name in MONITORING_API:
            self.assertRaises(APIError, api.get_fetch_method(name))

    def test_fetch_method(self):
        for name in MONITORING_API:
            response = api.get_fetch_method(name)()
            self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
