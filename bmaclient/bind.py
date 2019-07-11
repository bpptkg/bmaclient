import re
import six
import json
from six.moves.urllib.parse import quote

from .request import PlainRequest

re_path_template = re.compile('{\w+}')


def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)


class APIClientError(Exception):

    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message


class APIError(Exception):

    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message


def bind_method(**config):

    class MonitoringAPIMethod(object):

        path = config['path']
        method = config.get('method', 'GET')
        accepts_parameters = config.get('accepts_parameters', [])
        required_parameters = config.get('required_parameters', [])

        def __init__(self, api, **kwargs):
            self.api = api
            self.paginates = kwargs.get('page', None)
            self.parameters = {}

            self._check_required_parameters(kwargs)
            self._check_accepts_parameters(kwargs)
            self._build_parameters(kwargs)
            self._build_path()

        def _check_required_parameters(self, kwargs):
            for variable in self.required_parameters:
                if not kwargs.get(variable):
                    raise APIClientError('Parameter {} is required'.format(
                        variable))

        def _check_accepts_parameters(self, kwargs):
            for variable in self.accepts_parameters:
                if not kwargs.get(variable):
                    raise APIClientError(
                        'Parameter {} must be set before '
                        'calling the method'.format(variable))

        def _build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                try:
                    value = quote(self.parameters[name])
                except KeyError:
                    raise Exception(
                        'No parameter value found for path variable: {}'.format(name))
                del self.parameters[name]

                self.path = self.path.replace(variable, value)

        def _build_parameters(self, kwargs):
            for key, value in six.iteritems(kwargs):
                if value is None:
                    continue
                if key in self.parameters:
                    raise APIClientError(
                        "Parameter {} already supplied".format(key))
                self.parameters[key] = encode_string(value)

        def _do_api_request(self, url, method='GET', body=None, headers=None):
            headers = headers or {}
            response, content = PlainRequest(self.api).make_request(
                url, method=method, body=body, headers=headers)

            if response['status'] == '400':
                raise APIError(
                    response['status'],
                    'HTTP_BAD_REQUEST',
                    content)

            try:
                content_obj = json.loads(content.decode('utf-8'))
            except ValueError:
                raise APIClientError(
                    "Unable to parse response, not valid JSON.",
                    status_code=response['status'])

            if response['status'] == '200':
                if self.paginates:
                    results = content_obj['results']
                    next_url = content_obj['links']['next']
                    previous_url = content_obj['links']['previous']
                    return results, next_url, previous_url
                return content_obj, None, None
            else:
                raise APIError(response['status'],
                               'HTTP_SERVICE_UNAVAILABLE',
                               content)

        def execute(self):
            url, method, body, headers = PlainRequest(self.api).prepare_request(
                self.method, self.path, self.parameters)
            content, next_url, previous_url = self._do_api_request(
                url, method, body, headers)
            if self.paginates:
                return content, next_url, previous_url
            return content

    def _call_method(api, *args, **kwargs):
        method = MonitoringAPIMethod(api, *args, **kwargs)
        return method.execute()

    return _call_method