# ydapi_sdk/client.py
import time
import requests
from .exceptions import (NetworkError, TimeoutError, HTTPError, InvalidResponseError,
                         TrackingError, MySDKError, InvalidApiKeyError)
from .tracker import RequestTracker
import logging

# 配置日志记录
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class YdSDKClient:
    def __init__(self, api_key, tracking_url="http://ydapi.free.idcfengye.com/api/v1/track",
                 validation_url="http://ydapi.free.idcfengye.com/api/v1/apikey/validate"):
        self.api_key = api_key
        self.tracker = RequestTracker(tracking_url, api_key)
        self.validation_url = validation_url
        try:
            self._validate_api_key()
        except InvalidApiKeyError as e:
            print(f"Error: {e.message}")
            raise
        except MySDKError as e:
            print(f"An unexpected error occurred during API key validation: {e.message}")
            raise

    def _validate_api_key(self):
        """验证 API Key 的有效性"""
        payload = {"secretKey": self.api_key}
        headers = {"Content-Type": "application/json"}
        try:
            response = self._send_request("POST", self.validation_url, json=payload, headers=headers)
            if not response.get("success"):
                raise InvalidApiKeyError(response.get("message"))
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(str(e))
        except requests.exceptions.Timeout as e:
            raise TimeoutError(str(e))
        except requests.exceptions.HTTPError as e:
            raise HTTPError(e.response.status_code, e.response.text)
        except requests.exceptions.RequestException as e:
            raise MySDKError(str(e))
        except ValueError as e:
            raise InvalidResponseError(str(e))

    def _send_request(self, method, url, params=None, data=None, json=None, files=None, headers=None):
        """封装 requests.request 调用，统一处理请求异常"""
        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                files=files,
                headers=headers,
                timeout=10,
                verify=True
            )
            response.raise_for_status()
            return self._parse_response(response)
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(str(e))
        except requests.exceptions.Timeout as e:
            raise TimeoutError(str(e))
        except requests.exceptions.HTTPError as e:
            raise HTTPError(e.response.status_code, e.response.text)
        except requests.exceptions.RequestException as e:
            raise MySDKError(str(e))

    @staticmethod
    def _parse_response(response):
        """根据 Content-Type 解析响应体"""
        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                return response.json()
            elif "text/" in content_type:
                return response.text
            else:
                return response.content
        except ValueError as e:
            raise InvalidResponseError(str(e))

    def _make_request(self, method, url, params=None, data=None, json=None, files=None, headers=None):
        """
        发送请求并追踪它。

        :param method: HTTP 方法（GET、POST、PUT、DELETE 等）
        :param url: 请求的 URL
        :param params: 查询参数（字典）
        :param data: 表单数据（字典）
        :param json: JSON 数据（字典）
        :param files: 文件数据（字典）
        :param headers: 自定义请求头（字典）
        :return: 解析后的响应数据（JSON、文本或二进制）
        """
        start_time = time.time()
        response = None
        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                files=files,
                headers=headers,
                timeout=10,
                verify=True
            )
            response.raise_for_status()
            return self._parse_response(response)
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(str(e))
        except requests.exceptions.Timeout as e:
            raise TimeoutError(str(e))
        except requests.exceptions.HTTPError as e:
            raise HTTPError(e.response.status_code, e.response.text)
        except requests.exceptions.RequestException as e:
            raise MySDKError(str(e))
        finally:
            response_time_ms = int((time.time() - start_time) * 1000)
            try:
                self.tracker.track_request(
                    method=method,
                    url=url,
                    params=params if params is not None else {},
                    data=data if data is not None else (json if json is not None else {}),
                    response_status_code=response.status_code if response else None,
                    response_time_ms=response_time_ms
                )
            except Exception as e:
                raise TrackingError(str(e))

    def get(self, url, params=None, headers=None):
        """发送 GET 请求。"""
        return self._make_request("GET", url, params=params, headers=headers)

    def post(self, url, data=None, json=None, files=None, headers=None):
        """发送 POST 请求。"""
        return self._make_request("POST", url, data=data, json=json, files=files, headers=headers)

    def put(self, url, data=None, json=None, files=None, headers=None):
        """发送 PUT 请求。"""
        return self._make_request("PUT", url, data=data, json=json, files=files, headers=headers)

    def delete(self, url, headers=None):
        """发送 DELETE 请求。"""
        return self._make_request("DELETE", url, headers=headers)

    def patch(self, url, data=None, json=None, headers=None):
        """发送 PATCH 请求。"""
        return self._make_request("PATCH", url, data=data, json=json, headers=headers)