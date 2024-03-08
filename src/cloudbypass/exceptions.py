
class APIError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, **kwargs):
        self.message = kwargs.get("detail") or "Unknown Error"

    def __str__(self):
        return self.message



class BypassError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id") or "Unknown"
        self.code = kwargs.get("code") or "Unknown"
        self.message = kwargs.get("message") or "Unknown Error"

    def __str__(self):
        return f"{self.id}: {self.code} - {self.message}"


class BypassRequestError(BypassError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """


class BypassFailedError(BypassError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """


class BypassTimeoutError(BypassError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """


class BypassServerError(BypassError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """
