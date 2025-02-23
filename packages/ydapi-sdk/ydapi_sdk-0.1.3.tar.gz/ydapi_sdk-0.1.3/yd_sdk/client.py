# yd_sdk/client.py

import time
import requests
from .exceptions import NetworkError, TimeoutError, HTTPError, InvalidResponseError, TrackingError, MySDKError
from .tracker import RequestTracker

class YdSDKClient:
    def __init__(self, api_key, tracking_url="http://ydapi.free.idcfengye.com/api/v1/track"):
        self.api_key = api_key
        self.tracker = RequestTracker(tracking_url, api_key)

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
        response = None  # Initialize response to None
        start_time = time.time()  # 记录请求开始时间
        try:
            # 发送请求
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                files=files,
                headers=headers,
                timeout=10,  # 设置超时时间
            )
            response.raise_for_status()  # 检查 HTTP 错误

            # 根据 Content-Type 解析响应体
            content_type = response.headers.get("Content-Type", "")
            try:
                if "application/json" in content_type:
                    return response.json()  # 返回 JSON 数据
                elif "text/" in content_type:
                    return response.text  # 返回文本数据
                else:
                    return response.content  # 返回二进制数据
            except ValueError as e:
                raise InvalidResponseError(f"Failed to parse response: {e}")

        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Network error: {e}")
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out: {e}")
        except requests.exceptions.HTTPError as e:
            raise HTTPError(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise MySDKError(f"Request failed: {e}")
        finally:
            # 计算响应时间（毫秒）
            response_time_ms = int((time.time() - start_time) * 1000)
            # 追踪请求
            try:
                self.tracker.track_request(
                    method=method,
                    url=url,
                    params=params if params is not None else {},
                    data=data if data is not None else (json if json is not None else {}),
                    response_status_code=response.status_code if response else None,
                    response_time_ms=response_time_ms,  # 添加响应时间
                )
            except Exception as e:
                raise TrackingError(f"Tracking failed: {e}")

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