"""
Utilities related to deprecation of functions, methods, classes, and other
functionality.
"""

import re
import warnings

from .exceptions import BMADeprecationWarning
from .langhelpers import inject_docstring_text


def _warn_with_version(msg, version, type_, stacklevel):
    warn = type_(msg)
    warn.deprecated_since = version

    warnings.warn(warn, stacklevel=stacklevel + 1)


def warn_deprecated(msg, version, stacklevel=3):
    _warn_with_version(msg, version, BMADeprecationWarning, stacklevel)


def _sanitize_restructured_text(text):
    def repl(m):
        type_, name = m.group(1, 2)
        if type_ in ("func", "meth"):
            name += "()"
        return name

    text = re.sub(r":ref:`(.+) <.*>`", lambda m: '"%s"' % m.group(1), text)
    return re.sub(r"\:(\w+)\:`~?(?:_\w+)?\.?(.+?)`", repl, text)


def _decorate_with_warning(func, wtype, msg, version, docstring_header=None):
    """Wrap a function with a warnings.warn and augmented docstring."""

    message = _sanitize_restructured_text(msg)

    def warned(*args, **kwargs):
        skip_warning = kwargs.pop('_bma_skip_warning', False)
        if not skip_warning:
            _warn_with_version(message, version, wtype, stacklevel=3)
        return func(*args, **kwargs)

    doc = func.__doc__ is not None and func.__doc__ or ''
    if docstring_header is not None:
        docstring_header %= dict(func=func.__name__)

        doc = inject_docstring_text(doc, docstring_header, 1)

    decorated = warned
    decorated.__doc__ = doc
    decorated._bma_warn = lambda: _warn_with_version(
        message, version, wtype, stacklevel=3)
    return decorated


def _decorate_cls_with_warning(
    cls, constructor, wtype, msg, version, docstring_header=None
):
    """Decorate a class with warnings.warn and augmented docstring."""

    doc = cls.__doc__ is not None and cls.__doc__ or ''
    if docstring_header is not None:
        docstring_header %= dict(func=constructor)
        doc = inject_docstring_text(doc, docstring_header, 1)

        if type(cls) is type:
            clsdict = dict(cls.__dict__)
            clsdict['__doc__'] = doc
            clsdict.pop('__dict__', None)
            cls = type(cls.__name__, cls.__bases__, clsdict)
            constructor_fn = clsdict[constructor]
        else:
            cls.__doc__ = doc
            constructor_fn = getattr(cls, constructor)

        setattr(
            cls,
            constructor,
            _decorate_with_warning(constructor_fn, wtype, msg, version, None),
        )

    return cls


def deprecated_cls(version, msg, constructor='__init__'):
    message = msg or ''
    header = ".. deprecated:: {version} {message}".format(
        version=version, message=message)

    def decorate(cls):
        return _decorate_cls_with_warning(
            cls,
            constructor,
            BMADeprecationWarning,
            message % dict(func=constructor),
            version,
            header,
        )

    return decorate


def deprecated(version, message=None, add_deprecation_to_docstring=True, warning=None):
    """
    Decorates a function and issues a deprecation warning on use.
    """
    if add_deprecation_to_docstring:
        header = ".. deprecated:: {version} {message}".format(
            version=version, message=message or '')
    else:
        header = None

    if message is None:
        message = "Call to deprecated function %(func)s"

    if warning is None:
        warning = BMADeprecationWarning

    if warning is BMADeprecationWarning:
        message += ' (deprecated since: {})'.format(version)

    def decorate(fn):
        return _decorate_with_warning(
            fn, warning, message % dict(func=fn.__name__), version, header
        )

    return decorate
