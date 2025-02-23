# tests/test_client.py

import unittest
from yd_sdk.client import YdSDKClient

class TestYdSDKClientRealAPI(unittest.TestCase):
    def setUp(self):
        # 初始化 SDK 客户端
        self.client = YdSDKClient(api_key="test_key")

    def test_get_say(self):
        """
        测试 /api/say 接口。
        该接口返回纯文本，无需参数。
        """
        # 发送 GET 请求
        url = "https://uapis.cn/api/say"
        response = self.client.get(url)

        # 打印响应以便调试
        print("API Response (/api/say):", response)

        # 验证响应是否为纯文本
        self.assertIsInstance(response, str, "API request failed: Expected plain text response")

    def test_get_weather(self):
        """
        测试 /api/weather 接口。
        该接口需要查询参数（如城市名称）。
        """
        # 发送 GET 请求
        url = "https://uapis.cn/api/weather"
        params = {"name": "北京市"}  # 查询参数
        response = self.client.get(url, params=params)

        # 打印响应以便调试
        print("API Response (/api/weather):", response)

        # 验证状态码是否为 200（表示成功）
        self.assertEqual(response.get("code"), 200, "API request failed: Expected status code 200")

if __name__ == "__main__":
    unittest.main()