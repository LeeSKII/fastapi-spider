import requests
def get_weather_data(url:str):
    try:
        response = requests.get(url)
        # 检查请求是否成功
        response.raise_for_status()
        # 尝试将响应解析为JSON
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求异常: {e}")
        return None
