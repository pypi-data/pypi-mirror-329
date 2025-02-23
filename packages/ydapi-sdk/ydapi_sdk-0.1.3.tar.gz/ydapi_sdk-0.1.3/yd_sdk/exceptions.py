# yd_sdk/exceptions.py

class MySDKError(Exception):
    """Base exception for all SDK errors."""
    pass

class NetworkError(MySDKError):
    """Raised when a network-related error occurs."""
    pass

class TimeoutError(MySDKError):
    """Raised when a request times out."""
    pass

class HTTPError(MySDKError):
    """Raised when an HTTP error occurs."""
    pass

class InvalidResponseError(MySDKError):
    """Raised when the response cannot be parsed."""
    pass

class TrackingError(MySDKError):
    """Raised when tracking a request fails."""
    pass