"""
Encoder module provides utilities to encode query parameters in the request.
"""

import datetime

from .utils import encode_string


def encode_basestring(s):
    return encode_string(s, encoding='utf-8')


def encode_basestring_ascii(s):
    return encode_string(s, encoding='ascii')


class ParameterEncoder(object):
    """
    Extensible query parameters encoder.

    This class encodes the query parameter value to bytes string. Default
    behaviour is explained as follows:

    - list, tuple

    It will be encoded to bytes string of comma separated values. For example:
    ::

        [1, 2, 3] -> b'1,2,3'
        ['a', 'b', 'c'] -> b'a,b,c'

    - str

    str value will be encoded to bytes string. For example: ::

        'param' -> b'param'

    - bytes

    Bytes value will not be touch and returned as it is.

    - int, float

    int or float value will be encoded to bytes string. For example: ::

        12 -> b'12'
        14.56 -> b'14.56'

    - bool

    Boolean type will be encoded to bytes string with lower case value. For
    example: ::

        True -> b'true'
        False -> b'false'

    - None

    None value will be encoded to empty bytes string. For example: ::

        None -> b''

    - datetime.date

    Date object will be encoded to bytes string of date. Default format is
    '%Y-%m-%d'. For example: ::

        datetime.date(2020, 1, 1) -> b'2020-01-01'

    - datetime.datetime

    Datetime object will be encoded to bytes string of datetime. Default format
    is '%Y-%m-%d %H:%M:%M'. For example: ::

        datetime.datetime(2020, 1, 1, 9, 46, 12) -> b'2020-01-01 09:46:12'

    Note that BMA currently doesn't support ISO date format in the URL query
    parameters.

    - other

    Other values will be converted to string with ``str`` function and encoded
    with ASCII encoding unless default function is provided.
    """

    item_separator = ','
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, *, ensure_ascii=True, separator=None, date_format=None,
                 datetime_format=None, default=None):
        """
        Constructor of ParameterEncoder, with defaults.

        If ensure_ascii is True, the output is guaranteed to be str objects with
        all incoming non-ASCII characters escaped.  If ensure_ascii is false,
        the output can contain non-ASCII characters.

        If separator specified, it will be used for joining all strings in the
        list or tuple. Default to , (comma).

        If date_format specified, it will be used for converting date object to
        string. Default to ``%Y-%m-%d``.

        If datetime_format specified, it will be used for converting datetime
        object to string. Default to ``%Y-%m-%d %H:%M:%S``.

        If default specified, it is a function that gets called for objects that
        can't otherwise be encoded.  It should return an encodable version of
        the object or raise a ``TypeError``.
        """

        self.ensure_ascii = ensure_ascii
        if separator is not None:
            self.item_separator = separator
        if default is not None:
            self.default = default
        if date_format is not None:
            self.date_format = date_format
        if datetime_format is not None:
            self.datetime_format = datetime_format

    # pylint: disable=method-hidden
    def default(self, o):
        """
        Implement this method in a subclass such that it returns an encoded
        object for ``o``, or calls the base implementation (to raise a
        ``TypeError``).
        """
        raise TypeError('Object of type {} '
                        'is not serializable.'.format(o.__class__.__name__))

    def encode(self, o):
        """
        Return an encoded value of ``o`` object.
        """
        if isinstance(o, (list, tuple)):
            obj = [self._iterencode(i) for i in o]
            separator = bytes(self.item_separator, encoding='ascii')
            obj = separator.join(obj)
            if self.ensure_ascii:
                return encode_basestring_ascii(obj)
            else:
                return encode_basestring(obj)
        return self._iterencode(o)

    def encode_str(self, o):
        if self.ensure_ascii:
            return encode_basestring_ascii(o)
        return encode_basestring(o)

    def encode_bytes(self, o):
        return o

    def encode_none(self, o):
        return b''

    def encode_bool(self, o):
        return encode_basestring_ascii(o).lower()

    def encode_date(self, o):
        return encode_basestring_ascii(o.strftime(self.datetime_format))

    def encode_datetime(self, o):
        return encode_basestring_ascii(o.strftime(self.date_format))

    def encode_number(self, o):
        return encode_basestring_ascii(o)

    def _iterencode(self, o):
        if isinstance(o, str):
            return self.encode_str(o)

        if isinstance(o, bytes):
            return self.encode_bytes(o)

        if o is None:
            return self.encode_none(o)

        # Boolean True object is also an instance of int, so we need to check it
        # first.
        if isinstance(o, bool):
            return self.encode_bool(o)
        elif isinstance(o, (int, float)):
            return self.encode_number(o)

        # This must comes first before datetime.date because datetime.datetime
        # is an instance of datetime.date but not otherwise.
        if isinstance(o, datetime.datetime):
            return self.encode_date(o)
        elif isinstance(o, datetime.date):
            return self.encode_datetime(o)

        if self.default is not None:
            return self.default(o)
        return encode_basestring_ascii(o)
