import unittest
from ydapi_sdk.client import YdSDKClient


class TestYdSDKClientRealAPI(unittest.TestCase):
    def setUp(self):
        # 初始化SDK客户端
        self.client = YdSDKClient(api_key="ompdUdt5-ipAok7nZEddXjhQhMn2a2FwfwT3dhrN640")

    def test_get_say(self):
        """
        测试 /api/say接口。
        该接口返回纯文本，无需参数。
        """
        # 发送GET请求
        url = "https://uapis.cn/api/say"
        try:
            response = self.client.get(url)
            # 打印响应以便调试
            print("API Response (/api/say):", response)
            # 验证响应是否为纯文本
            self.assertIsInstance(response, str, "API request failed: Expected plain text response")
        except Exception as e:
            self.fail(f"API request failed with error: {e}")

    def test_get_weather(self):
        """
        测试 /api/weather接口。
        该接口需要查询参数（如城市名称）。
        """
        # 发送GET请求
        url = "https://uapis.cn/api/weather"
        params = {"name": "北京市"}  # 查询参数
        try:
            response = self.client.get(url, params=params)
            # 打印响应以便调试
            print("API Response (/api/weather):", response)
            # 验证状态码是否为200（表示成功）
            # 这里假设接口返回的是JSON格式且包含code字段
            if isinstance(response, dict):
                self.assertEqual(response.get("code"), 200, "API request failed: Expected status code 200")
            else:
                self.fail("API request failed: Unexpected response format")
        except Exception as e:
            self.fail(f"API request failed with error: {e}")


if __name__ == "__main__":
    unittest.main()