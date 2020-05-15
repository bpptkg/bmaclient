import os
import six

from .models import DataModel


def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)


def object_from_list(entry):
    """Objectify item in a list of dictionary."""
    return [DataModel(**item) for item in entry]


def get_api_key(name='API_KEY'):
    """Read API key from OS environment variables."""
    API_KEY = os.environ.get(name)
    if API_KEY is None:
        raise ValueError(
            'Could not get {} from OS environment variables'.format(name))
    return API_KEY


def get_access_token(name='ACCESS_TOKEN'):
    """Read OAuth2 access token from OS environment variables."""
    ACCESS_TOKEN = os.environ.get(name)
    if ACCESS_TOKEN is None:
        raise ValueError(
            'Could not get {} from OS environment variables'.format(name))
    return ACCESS_TOKEN


def encode_parameters(kwargs):
    """Encode URL parameters dictionary."""
    params = {}
    for key, value in six.iteritems(kwargs):
        if value is None:
            continue
        params[key] = encode_string(value)
    return params
