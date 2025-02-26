# ydapi_sdk/exceptions.py
import logging

# 配置日志记录
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MySDKError(Exception):
    """Base exception for all SDK errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NetworkError(MySDKError):
    """Raised when a network-related error occurs."""
    def __init__(self, message):
        super().__init__(f"Network error: {message}")
        logger.error(self.message)


class TimeoutError(MySDKError):
    """Raised when a request times out."""
    def __init__(self, message):
        super().__init__(f"Request timed out: {message}")
        logger.error(self.message)


class HTTPError(MySDKError):
    """Raised when an HTTP error occurs."""
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"HTTP error: {status_code} - {response_text}")
        logger.error(self.message)


class InvalidResponseError(MySDKError):
    """Raised when the response cannot be parsed."""
    def __init__(self, error):
        super().__init__(f"Failed to parse response: {error}")
        logger.error(self.message)


class TrackingError(MySDKError):
    """Raised when tracking a request fails."""
    def __init__(self, message):
        super().__init__(f"Tracking failed: {message}")
        logger.error(self.message)


class InvalidApiKeyError(MySDKError):
    """Raised when the API key is invalid."""
    def __init__(self, message):
        super().__init__(f"API key is invalid: {message}")
        logger.error(self.message)
