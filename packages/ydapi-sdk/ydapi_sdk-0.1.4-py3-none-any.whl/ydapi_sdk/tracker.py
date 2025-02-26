# ydapi_sdk/tracker.py

import requests
from .exceptions import TrackingError

class RequestTracker:
    def __init__(self, tracking_url, api_key):
        self.tracking_url = tracking_url
        self.api_key = api_key

    def track_request(self, method, url, params=None, data=None, response_status_code=None, response_time_ms=None):
        """Send request details to the tracking server."""
        # 确保 params 和 data 不为 None
        payload = {
            "method": method,
            "url": url,
            "params": params if params is not None else {},
            "data": data if data is not None else {},
            "response_status_code": response_status_code,
            "api_key": self.api_key,
            "response_time_ms": response_time_ms,  # 添加响应时间
        }
        try:
            # 添加 Bearer Token 认证
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            response = requests.post(self.tracking_url, json=payload, headers=headers)

            # 检查状态码是否为 201
            if response.status_code != 201:
                raise TrackingError(f"Tracking failed: Unexpected status code {response.status_code}")

            # 解析响应体
            response_data = response.json()
            if not response_data.get("success"):
                raise TrackingError(f"Tracking failed: {response_data.get('message')}")

            # 返回成功消息
            return response_data.get("message")

        except requests.exceptions.RequestException as e:
            raise TrackingError(f"Failed to track request: {e}")