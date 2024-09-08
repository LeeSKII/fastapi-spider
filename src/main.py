import re
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
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

# TODO: 实现天气预报
@app.get('/weather/forecast/{city_id}')
async def weather(city_id:str):
    # 定义中文键名到英文键名的映射
    key_mapping = {
        '时间': 'time',
        '天气': 'weather',
        '气温': 'temperature',
        '降水': 'precipitation',
        '风速': 'wind_speed',
        '风向': 'wind_direction',
        '气压': 'pressure',
        '湿度': 'humidity',
        '云量': 'cloud_cover'
    }
    try:
        response = requests.get(f'https://weather.cma.cn/web/weather/{city_id}.html')
        if response.status_code == 200:
            html_content = BeautifulSoup(response.content, 'lxml')
            table = html_content.find('table', class_='hour-table')
            rows = table.find_all('tr')

            # 获取时间列表（列标题）
            time_slots = [td.text.strip() for td in rows[0].find_all('td')[1:]]

            # 初始化结果列表
            result = [{} for _ in time_slots]

            for row in rows:  # 跳过表头行
                cells = row.find_all('td')
                if cells:
                    key = cells[0].text.strip().replace('', '').replace(' ', '')
                    english_key = key_mapping.get(key, key)  # 使用映射获取英文键名
                    for i, cell in enumerate(cells[1:]):
                        if '天气' in key:
                            value = cell.find('img')['src'].split('/')[-1] if cell.find('img') else ''
                        else:
                            value = cell.text.strip()
                        result[i][english_key] = value
        

            return result
        else:
            return {"message": "Error: " + str(response.status_code)}
    except requests.exceptions.RequestException as e:
        return {"message": "Error: " + str(e)} 


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
    