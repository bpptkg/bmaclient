import unittest

from bmaclient.request import Request


class API(object):
    """
    API test class.
    """
    host = 'cendana15.com:8080'
    base_path = 'api/v1/'
    protocol = 'http'
    api_name = 'BPPTKG Monitoring API'
    authorize_url = 'http://cendana15.com:8080/oauth/authorize/'
    access_token_url = 'http://cendana15.com:8080/oauth/token/'
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
                         'http://cendana15.com:8080/api/v1/seismicity/')
        self.assertEqual(
            request._full_query_with_params(params),
            '?eventdate__gte=2020-01-01')
        self.assertEqual(request._full_url_with_params('seismicity/', params),
                         'http://cendana15.com:8080/api/v1/seismicity/'
                         '?eventdate__gte=2020-01-01')

        url, method, body, headers = request.prepare_request(
            'GET', 'seismicity/', params)
        self.assertEqual(url,
                         'http://cendana15.com:8080/api/v1/seismicity/'
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
        self.assertEqual(url, 'http://cendana15.com:8080/api/v1/slope/')
        self.assertEqual(method, 'POST')
        self.assertEqual(body, 'benchmark=BAB0')
        self.assertDictEqual(
            headers, {'Content-type': 'application/x-www-form-urlencoded'})


if __name__ == '__main__':
    unittest.main()
