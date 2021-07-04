import json
import re

import six
from six.moves.urllib.parse import quote

from .exceptions import APIClientError, APIError
from .request import Request
from .utils import object_from_list

ERROR_STATUS = {
    '400': 'HTTP_BAD_REQUEST',
    '403': 'HTTP_PERMISSION_DENIED',
    '404': 'HTTP_NOT_FOUND',
    '500': 'HTTP_SERVER_ERROR',
}

re_path_template = re.compile(r'{\w+}')


class MonitoringAPIMethod(object):
    """
    Monitoring API method object.
    """

    def __init__(self, config, api, *args, **kwargs):
        self.path = config['path']
        self.method = config.get('method', 'GET')
        self.accepts_parameters = config.get('accepts_parameters', [])
        self.required_parameters = config.get('required_parameters', [])
        self.doc = config.get('doc', '')

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
                raise APIClientError("Parameter '{}' is required.".format(
                    variable))

    def _check_accepts_parameters(self, kwargs):
        for variable in self.accepts_parameters:
            if not kwargs.get(variable):
                raise APIClientError(
                    "Parameter '{}' must be set before "
                    "calling the method.".format(variable))

    def _build_path(self):
        for variable in re_path_template.findall(self.path):
            name = variable.strip('{}')

            try:
                value = quote(self.parameters[name])
            except KeyError:
                raise Exception(
                    'No parameter value found '
                    'for path variable: {}'.format(name))
            del self.parameters[name]

            self.path = self.path.replace(variable, value)

    def _build_parameters(self, kwargs):
        encoder = self.api.encoder_class()
        for key, value in six.iteritems(kwargs):
            if value is None:
                continue
            if key in self.parameters:
                raise APIClientError(
                    "Parameter '{}' already supplied.".format(key))
            self.parameters[key] = encoder.encode(value)

    def _do_api_request(self, url, method='GET', body=None, headers=None):
        headers = headers or {}
        response, content = Request(self.api).make_request(
            url, method=method, body=body, headers=headers)

        if response['status'] in ERROR_STATUS:
            raise APIError(
                response['status'],
                ERROR_STATUS[response['status']],
                content)

        if content:
            try:
                content_obj = json.loads(content.decode('utf-8'))
            except ValueError:
                raise APIClientError(
                    "Unable to parse response, not valid JSON.",
                    status_code=response['status'])
        else:
            content_obj = None

        if response['status'] == '200':
            if self.paginates:
                if not content_obj:
                    return content_obj, None, None
                results = content_obj['results']
                next_url = content_obj['links']['next']
                previous_url = content_obj['links']['previous']
                return results, next_url, previous_url
            return content_obj, None, None
        elif response['status'] == '201':
            return content_obj, None, None
        elif response['status'] == '204':
            return content_obj, None, None
        else:
            raise APIError(response['status'],
                           'HTTP_SERVICE_UNAVAILABLE',
                           content)

    def execute(self):
        url, method, body, headers = Request(
            self.api).prepare_request(
            self.method, self.path, self.parameters)

        content, next_url, previous_url = self._do_api_request(
            url, method, body, headers)

        if self.paginates:
            if self.api.format == 'object':
                return object_from_list(content), next_url, previous_url
            return content, next_url, previous_url

        if self.api.format == 'object':
            return object_from_list(content)
        return content


def bind_method(**config):
    """Bind API object method."""

    def _call_method(api, *args, **kwargs):
        _return_as_instance = kwargs.pop('_return_as_instance', None)
        method = MonitoringAPIMethod(config, api, *args, **kwargs)
        if _return_as_instance:
            return method
        return method.execute()

    _call_method.__doc__ = config.get('doc', '')

    return _call_method
