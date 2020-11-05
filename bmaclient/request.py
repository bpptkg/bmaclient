import json

import six
from httplib2 import Http
from six.moves.urllib.parse import urlencode

from .utils import encode_parameters
from .version import __version__


class OAuth2AuthExchangeError(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class Request(object):
    """
    Class representing request object.
    """

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

    def get(self, path, **kwargs):
        return self.make_request(self.prepare_request('GET', path, kwargs))

    def post(self, path, **kwargs):
        return self.make_request(self.prepare_request('POST', path, kwargs))

    def put(self, path, **kwargs):
        return self.make_request(self.prepare_request('PUT', path, kwargs))

    def patch(self, path, **kwargs):
        return self.make_request(self.prepare_request('PATCH', path, kwargs))

    def delete(self, path, **kwargs):
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
            user_agent = '{} Python Client (version {})'.format(
                self.api.api_name, __version__)
            headers.update(
                {'User-Agent': user_agent,
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


class OAuth2API(object):

    host = None
    base_path = None
    protocol = 'http'
    api_name = 'OAuth2API'
    authorize_url = None
    redirect_uri = None
    access_token_url = None
    access_token_field = 'access_token'

    def __init__(self, **kwargs):
        self.client_id = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
        self.access_token = kwargs.get('access_token')
        self.redirect_uri = kwargs.get('redirect_uri')

    def get_authorize_url(self, scope=None):
        request = OAuth2AuthExchangeRequest(self)
        return request.get_authorize_url(scope=scope)

    def get_authorize_login_url(self, scope=None):
        request = OAuth2AuthExchangeRequest(self)
        return request.get_authorize_login_url(scope=scope)

    def exchange_code_for_access_token(self, code):
        request = OAuth2AuthExchangeRequest(self)
        return request.exchange_for_access_token(code=code)

    def exchange_xauth_login_for_access_token(self, username, password,
                                              scope=None):
        request = OAuth2AuthExchangeRequest(self)
        return request.exchange_for_access_token(
            username=username, password=password, scope=scope)


class OAuth2AuthExchangeRequest(object):

    def __init__(self, api):
        self.api = api

    def _url_for_authorize(self, scope=None):
        client_params = {
            'client_id': self.api.client_id,
            'response_type': 'code',
            'redirect_uri': self.api.redirect_uri
        }
        if scope:
            client_params.update(scope=' '.join(scope))
        url_params = urlencode(encode_parameters(client_params))
        return '{}?{}'.format(self.api.authorize_url, url_params)

    def _data_for_exchange(self, code=None, username=None, password=None,
                           scope=None):
        client_params = {
            'client_id': self.api.client_id,
            'client_secret': self.api.client_secret,
            'redirect_uri': self.api.redirect_uri,
            'grant_type': 'authorization_code'
        }
        if code:
            client_params.update(code=code)
        elif username and password:
            client_params.update(username=username, password=password,
                                 grant_type='password')
            if scope:
                client_params.update(scope=' '.join(scope))
        return urlencode(encode_parameters(client_params))

    def get_authorize_url(self, scope=None):
        return self._url_for_authorize(scope=scope)

    def get_authorize_login_url(self, scope=None):
        http_obj = Http(disable_ssl_certificate_validation=True)

        url = self._url_for_authorize(scope=scope)
        response, __ = http_obj.request(url)
        if response['status'] != '200':
            raise OAuth2AuthExchangeError(
                'The server returned a non-200 response for URL {}'.format(
                    url))
        redirected_to = response['content-location']
        return redirected_to

    def exchange_for_access_token(self, code=None, username=None,
                                  password=None, scope=None):
        data = self._data_for_exchange(code, username, password, scope)
        url = self.api.access_token_url
        http_obj = Http(disable_ssl_certificate_validation=True)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = http_obj.request(url, method='POST', body=data,
                                             headers=headers)
        parsed_content = json.loads(content.decode('utf-8'))
        if int(response['status']) != 200:
            raise OAuth2AuthExchangeError(
                parsed_content.get('error_message', ''))
        return response, parsed_content
