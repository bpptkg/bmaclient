import os
import six

from .models import DataModel


def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)


def object_from_list(entry):
    """Objectify item in a list of dictionary."""
    return [DataModel(**item) for item in entry]


def get_api_key():
    """Read API key from OS environment variables."""
    API_KEY = os.environ.get('API_KEY')
    if API_KEY is None:
        raise AssertionError(
            'Could not get API_KEY from OS environment variables')
    return API_KEY


def get_access_token():
    """Read OAuth2 access token from OS environment variables."""
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    if ACCESS_TOKEN is None:
        raise AssertionError(
            'Could not get ACCESS_TOKEN from OS environment variables')
    return ACCESS_TOKEN


def encode_parameters(kwargs):
    """Encode URL parameters dictionary."""
    params = {}
    for key, value in six.iteritems(kwargs):
        if value is None:
            continue
        params[key] = encode_string(value)
    return params
