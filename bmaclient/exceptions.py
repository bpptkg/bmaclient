class APIClientError(Exception):
    """
    Raises when there are an error on client side.
    """

    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message


class APIError(Exception):
    """
    Raises when there are an error on server side.
    """

    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message


class BMADeprecationWarning(DeprecationWarning):
    """
    Issued for usage of deprecated APIs.
    """
    deprecated_since = None


class BMAPendingDeprecationWarning(PendingDeprecationWarning):
    """
    A similar warning as :class:`bmaclient.exceptions.BMADeprecationWarning`,
    but for pending deprecation.
    """
    deprecated_since = None
