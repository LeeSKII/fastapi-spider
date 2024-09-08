import re
from fastapi import FastAPI
import requests
from utils.weather import get_weather_data

app = FastAPI()

@app.get('/spider')
async def spider():
    return {"message": "Hello, Spider!"}

@app.get('/weather/now/{city_id}')
async def weather(city_id:str):
	try:
		response = requests.get(f'https://weather.cma.cn/api/now/{city_id}')
		# 检查请求是否成功
		response.raise_for_status()
		
		# 尝试将响应解析为JSON
		data = response.json()
		
		return data
	except requests.exceptions.RequestException as e:
		return {"message": "Error: " + str(e)}
  
  
@app.get('/dict/province')
async def province_dict():
    url= 'https://weather.cma.cn/api/dict/province'
    data = get_weather_data(url)
    # 步骤1：按"|"分割字符串 python中使用[]获取dict中键值
    parts = data['data'].split("|")

	# 步骤2：创建一个列表来存储结果对象
    result = []

		# 步骤3：遍历分割后的部分，进一步处理
    for part in parts:
        # 按","分割每个部分
        code, name = part.split(",") if "," in part else (part, None)
        
        # 创建对象并添加到结果列表
        result.append({
            "code": code,
            "name": name
        })
    return result

@app.get('/dict/province/{province_code}')
async def province_dict(province_code:str):
    url= f'https://weather.cma.cn/api/dict/province/{province_code}'
    data = get_weather_data(url)
    # 步骤1：按"|"分割字符串 python中使用[]获取dict中键值
    parts = data['data'].split("|")

	# 步骤2：创建一个列表来存储结果对象
    result = []

		# 步骤3：遍历分割后的部分，进一步处理
    for part in parts:
        # 按","分割每个部分
        id, name = part.split(",") if "," in part else (part, None)
        
        # 创建对象并添加到结果列表
        result.append({
            "id": id,
            "name": name
        })
    return result

@app.get('/dict/country')
async def country():
    url = 'https://weather.cma.cn/api/dict/country'
    data = get_weather_data(url)
    parts = data['data'].split("|")
    result = []
    for part in parts:
        code, name = part.split(",") if "," in part else (part, None)
        result.append({
            "code": code,
            "name": name
        })
    return result

@app.get('/dict/country/{country_code}')
async def province_dict(country_code:str):
    url= f'https://weather.cma.cn/api/dict/country/{country_code}'
    data = get_weather_data(url)
    # 步骤1：按"|"分割字符串 python中使用[]获取dict中键值
    parts = data['data'].split("|")

	# 步骤2：创建一个列表来存储结果对象
    result = []

		# 步骤3：遍历分割后的部分，进一步处理
    for part in parts:
        # 按","分割每个部分
        id, name = part.split(",") if "," in part else (part, None)
        
        # 创建对象并添加到结果列表
        result.append({
            "id": id,
            "name": name
        })
    return result

@app.get('/map/weather/{day}')
async def weather_map(day:str):
	try:
		response = requests.get(f'https://weather.cma.cn/api/map/weather/{day}')
		# 检查请求是否成功
		response.raise_for_status()
		# 尝试将响应解析为JSON
		data = response.json()
		return data
	except requests.exceptions.RequestException as e:
		return {"message": "Error: " + str(e)}
    