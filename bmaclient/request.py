from six.moves.urllib.parse import urlencode
import six
from httplib2 import Http


class Request(object):

    def __init__(self, api):
        self.api = api

    def _full_url(self, path):
        return '{protocol}://{host}/{base_path}{path}'.format(
            protocol=self.api.protocol,
            host=self.api.host,
            base_path=self.api.base_path,
            path=path)

    def _full_url_with_params(self, path, params):
        return '{full_url}{full_query_with_params}'.format(
            full_url=self._full_url(path),
            full_query_with_params=self._full_query_with_params(params))

    def _full_query_with_params(self, params):
        params = '?{}'.format(urlencode(params)) if params else ''
        return params

    def _post_body(self, params):
        return urlencode(params)

    def url_for_get(self, path, parameters):
        return self._full_url_with_params(path, parameters)

    def get_request(self, path, **kwargs):
        return self.make_request(self.prepare_request('GET', path, kwargs))

    def post_request(self, path, **kwargs):
        return self.make_request(self.prepare_request('POST', path, kwargs))

    def put_request(self, path, **kwargs):
        return self.make_request(self.prepare_request('PUT', path, kwargs))

    def patch_request(self, path, **kwargs):
        return self.make_request(self.prepare_request('PATCH', path, kwargs))

    def delete_request(self, path, **kwargs):
        return self.make_request(self.prepare_request('DELETE', path, kwargs))

    def prepare_request(self, method, path, params):
        url = None
        body = None
        headers = {}

        if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            body = self._post_body(params)
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            url = self._full_url(path)
        else:
            url = self._full_url_with_params(path, params)

        return url, method, body, headers

    def make_request(self, url, method='GET', body=None, headers=None):
        headers = headers or {}
        if not 'User-Agent' in headers:
            headers.update(
                {'User-Agent': '{} Python Client'.format(self.api.api_name),
                 'Connection': 'close'})
        if self.api.api_key:
            headers.update(
                {'Authorization': 'Api-Key {}'.format(self.api.api_key)})
        else:
            if self.api.access_token:
                headers.update({
                    'Authorization': 'Bearer {}'.format(self.api.access_token)
                })
        http_obj = Http() if six.PY3 else Http(
            disable_ssl_certificate_validation=True)
        return http_obj.request(url, method, body=body, headers=headers)
