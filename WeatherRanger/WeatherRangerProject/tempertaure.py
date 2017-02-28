import requests
import json
import pandas as pd
import requests
import subprocess
from io import StringIO, BytesIO
#from WeatherRangerProject.models import City
import gzip
API_KEY = '8e662200ba6ef23c0cc1c12a3aeaf9e3'
URL_TEMPLATE = "http://api.openweathermap.org/data/2.5/weather?id={}&appid={}"
CITY_LIST_URL = "http://bulk.openweathermap.org/sample/city.list.json.gz"
CITY_US_LIST_URL = "http://bulk.openweathermap.org/sample/city.list.us.json.gz"
FORECAST_URL_TEMPLATE = "http://api.openweathermap.org/data/2.5/forecast/daily?id={}&appid={}&cnt={}"

def get_temperature(id):
    url = URL_TEMPLATE.format(str(id), API_KEY)
    print(url)
    response = requests.get(url)
    print(response.text)
    return json.loads(response.text)

def get_temperature_simple(id):
    try:
        data = get_temperature(id)
        return round(data['main']['temp'] - 273, 2)
    except:
        print('failed to get data')
        return 0


def get_forecast(id, days):
    url = FORECAST_URL_TEMPLATE.format(str(id), API_KEY, days)
    print(url)
    response = requests.get(url)
    return json.loads(response.text)

def get_sixteen_day_forcast(id):
    return get_forecast(id, days=16)

def on_board_cites():
    subprocess.call('wget ' + CITY_US_LIST_URL, shell=True)

    g_file = gzip.GzipFile('city.list.us.json.gz')
    raw_data = str(g_file.read())
    print(raw_data.split())




def calculate_upper_lower(id, days, n=2):
    data = get_forecast(id, days)
    weather_list = data['list']
    temp_list = [sum((d['temp'].values()))/len(d['temp'].values()) for d in weather_list]
    print(temp_list)
    return find_upper_and_lower(temp_list, n=n)

def calculate_five_day_upper_lower(id):
    return calculate_upper_lower(id, 5)

def calculate_sixteen_day_upper_lower(id):
    return calculate_upper_lower(id, 16, n=4)


def find_upper_and_lower(weather_range, n=2): #default of two day moving average
    total = 0
    avg_array = []
    for day_num, weather in enumerate(weather_range):
        total += weather
        if day_num + 1 < n:
            continue
        avg = total/n
        last = weather_range[day_num + 1 - n]
        total -= last
        avg_array.append(avg)

    upper = max(avg_array) - 273
    lower = min(avg_array) - 273
    print(upper, lower)
    return upper , lower



if __name__ == '__main__':
    #print(get_temperature(5128638))
    #print(pd.DataFrame(calculate_five_day(5128638)['list']).to_csv('sample_temp.csv'))
    #print(calculate_five_day_upper_lower(5128638))
    #print(calculate_sixteen_day_upper_lower(5128638))
    on_board_cites()