# yd_sdk

这个sdk用于ydapi平台记录api访问数据，方便用户便捷使用和分析接口的访问情况

## 安装

1. 从[这里](https://github.com/firework-a/ydapi_sdk-0.1.0.tar.gz)下载SDK包 .
2. 使用pip安装软件包:
   ```bash
   pip install ydapi-sdk
   ```

3. 安装依赖项:
   ```bash
   pip install requests
   ```

## 集成示例

```python
# 导入 YdSDKClient 类
from yd_sdk.client import YdSDKClient

# 初始化 SDK 客户端
api_key = "your_api_key"
client = YdSDKClient(api_key)


# 1. 发送 GET 请求
def send_get_request():
    url = "https://example.com/api/data"
    params = {
        "param1": "value1",
        "param2": "value2"
    }
    headers = {
        "Custom-Header": "Custom-Value"
    }
    try:
        response = client.get(url, params=params, headers=headers)
        print("GET 请求响应:", response)
    except Exception as e:
        print("GET 请求出错:", e)


# 2. 发送 POST 请求
def send_post_request():
    url = "https://example.com/api/create"
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    headers = {
        "Custom-Header": "Custom-Value"
    }
    try:
        response = client.post(url, data=data, headers=headers)
        print("POST 请求响应:", response)
    except Exception as e:
        print("POST 请求出错:", e)


# 3. 发送 PUT 请求
def send_put_request():
    url = "https://example.com/api/update/1"
    json_data = {
        "field1": "new_value1",
        "field2": "new_value2"
    }
    headers = {
        "Custom-Header": "Custom-Value"
    }
    try:
        response = client.put(url, json=json_data, headers=headers)
        print("PUT 请求响应:", response)
    except Exception as e:
        print("PUT 请求出错:", e)


# 4. 发送 DELETE 请求
def send_delete_request():
    url = "https://example.com/api/delete/1"
    headers = {
        "Custom-Header": "Custom-Value"
    }
    try:
        response = client.delete(url, headers=headers)
        print("DELETE 请求响应:", response)
    except Exception as e:
        print("DELETE 请求出错:", e)


# 5. 发送 PATCH 请求
def send_patch_request():
    url = "https://example.com/api/partial-update/1"
    json_data = {
        "field1": "updated_value1"
    }
    headers = {
        "Custom-Header": "Custom-Value"
    }
    try:
        response = client.patch(url, json=json_data, headers=headers)
        print("PATCH 请求响应:", response)
    except Exception as e:
        print("PATCH 请求出错:", e)


# 执行各个请求示例
send_get_request()
send_post_request()
send_put_request()
send_delete_request()
send_patch_request()
```