import os

import six

from .models import DataModel


def encode_string(s, encoding='utf-8', errors='strict'):
    """Encode string s to bytes."""
    if isinstance(s, bytes):
        return s
    if isinstance(s, six.text_type):
        s = s.encode(encoding, errors=errors)
    else:
        s = str(s).encode(encoding, errors=errors)
    return s


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


def get_api_key_from_file(path, strict=False):
    """
    Read API key from file.

    The file can contains a comment that starts with hash character (#).
    Otherwise, the first line that is not a comment would be treated as API key
    value. It also returns empty string if file is empty.

    If strict is True, raise ValueError when API key value is empty.
    """
    if not os.path.isfile(path):
        raise ValueError('File is not exists: {}'.format(path))

    COMMENT = '#'
    with open(path, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            if not line.startswith(COMMENT):
                return line
    if strict:
        raise ValueError('Could not get API key from file: {}'.format(path))
    return ''
