import unittest

from bmaclient.request import Request


class API(object):
    """
    API test class.
    """
    host = 'bma.cendana15.com'
    base_path = 'api/v1/'
    protocol = 'https'
    api_name = 'BPPTKG Monitoring API'
    authorize_url = 'https://bma.cendana15.com/oauth/authorize/'
    access_token_url = 'https://bma.cendana15.com/oauth/token/'
    access_token_field = 'access_token'
    redirect_uri = None


class RequestTest(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def test_urls(self):
        request = Request(self.api)

        # Using multiple entries may fail because dict is unordered. So test
        # using only one parameter.
        params = {'eventdate__gte': '2020-01-01'}
        self.assertEqual(request._full_url('seismicity/'),
                         'https://bma.cendana15.com/api/v1/seismicity/')
        self.assertEqual(
            request._full_query_with_params(params),
            '?eventdate__gte=2020-01-01')
        self.assertEqual(request._full_url_with_params('seismicity/', params),
                         'https://bma.cendana15.com/api/v1/seismicity/'
                         '?eventdate__gte=2020-01-01')

        url, method, body, headers = request.prepare_request(
            'GET', 'seismicity/', params)
        self.assertEqual(url,
                         'https://bma.cendana15.com/api/v1/seismicity/'
                         '?eventdate__gte=2020-01-01')
        self.assertEqual(method, 'GET')
        self.assertIsNone(body)
        self.assertDictEqual(headers, dict())

    def test_post_body(self):
        request = Request(self.api)

        # Using multiple entries may fail because dict is unordered. So test
        # using only one parameter.
        params = {
            'benchmark': 'BAB0',
        }
        url, method, body, headers = request.prepare_request(
            'POST', 'slope/', params)
        self.assertEqual(url, 'https://bma.cendana15.com/api/v1/slope/')
        self.assertEqual(method, 'POST')
        self.assertEqual(body, 'benchmark=BAB0')
        self.assertDictEqual(
            headers, {'Content-type': 'application/x-www-form-urlencoded'})


if __name__ == '__main__':
    unittest.main()
