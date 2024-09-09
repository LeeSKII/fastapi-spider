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
    baseUrl = 'https://weather.cma.cn'
    try:
        response = requests.get(f'https://weather.cma.cn/web/weather/{city_id}.html')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
           # Find the div with id 'dayList'
            day_list = soup.find('div', id='dayList')

            # Find all hour tables
            hour_tables = soup.find_all('table', class_='hour-table')

            # Initialize the result list
            weather_data = []

            # Process each day's data
            for day, hour_table in zip(day_list.find_all('div', class_=lambda x: x and 'pull-left day' in x), hour_tables):
                day_data = {}
                
                # Extract day information
                date_info = day.find('div', class_='day-item').text.strip().split('\n')
                day_data['weekday'] = date_info[0].strip()
                day_data['date'] = date_info[1].strip()
                day_data['day_weather'] = day.find_all('div', class_='day-item')[2].text.strip()
                day_data['day_wind'] = day.find_all('div', class_='day-item')[3].text.strip()
                day_data['day_wind_strength'] = day.find_all('div', class_='day-item')[4].text.strip()
                day_data['high_temp'] = day.find('div', class_='high').text.strip()
                day_data['low_temp'] = day.find('div', class_='low').text.strip()
                day_data['night_weather'] = day.find_all('div', class_='day-item')[-3].text.strip()
                day_data['night_wind'] = day.find_all('div', class_='day-item')[-2].text.strip()
                day_data['night_wind_strength'] = day.find_all('div', class_='day-item')[-1].text.strip()
                
                # Extract hourly data
                hourly_data = []
                rows = hour_table.find_all('tr')
                headers = [th.text.strip() for th in rows[0].find_all('td')[1:]]
                
                for row in rows:
                    cells = row.find_all('td')[1:]
                    data_type = row.find('td').text.strip()
                    for i, cell in enumerate(cells):
                        if i >= len(hourly_data):
                            hourly_data.append({})
                        if data_type == '天气':
                            hourly_data[i][key_mapping.get(data_type, data_type)] = baseUrl+cell.find('img')['src']
                        else:
                            hourly_data[i][key_mapping.get(data_type, data_type)] = cell.text.strip()
                
                day_data['hourly_data'] = hourly_data
                weather_data.append(day_data)
        

            return weather_data
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
    