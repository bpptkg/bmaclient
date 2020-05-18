import unittest

from bmaclient.client import MonitoringAPI
from bmaclient.bind import APIClientError, MonitoringAPIMethod


class BindMethodTest(unittest.TestCase):
    def setUp(self):
        self.api = MonitoringAPI()

    def test_bind(self):
        method = self.api.fetch_doas(return_as_instance=True)
        self.assertEqual(method.path, 'doas/')
        self.assertTrue(isinstance(method, MonitoringAPIMethod))

        method = self.api.fetch_gps_position(station='pasarbubar',
                                             timestamp__gte='2020-01-01',
                                             timestamp__lt='2020-02-01',
                                             nolimit=True,
                                             return_as_instance=True)
        self.assertEqual(method.path, 'gps/position/pasarbubar/')
        self.assertDictEqual(method.parameters, {
            'timestamp__gte': b'2020-01-01',
            'timestamp__lt': b'2020-02-01',
            'nolimit': b'True',
        })

    def test_check_required_parameters(self):
        with self.assertRaises(APIClientError):
            method = self.api.fetch_gps_baseline(return_as_instance=True)

    def test_accepts_parameters(self):
        with self.assertRaises(APIClientError):
            method = self.api.fetch_tiltmeter(return_as_instance=True)


if __name__ == '__main__':
    unittest.main()
