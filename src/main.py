"""
Armando De La Rosa - April,2022

This Script purpose is to run and
inject weather data of certain cities
into influxdata.com
"""
from configparser import ConfigParser
import sys
import pytz
from datetime import datetime
import requests
import json
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def logger(path: str, job_name: str, message: str, status: bool) -> None:
    '''
    path     - File Path where the .txt will be stored
    job_name - Descriptive name for the main.py
    message  - Describe the logged action
    status   - Input = 1, Success 
             - Input = 0, Error
    '''
    current_time = datetime.now(pytz.timezone('America/Mexico_City') ).strftime('%d/%m/%Y %H:%M:%S')
    file_object = open(path + 'logs.txt', 'a')
    file_object.write('\n\n\nJob Name: ' + job_name + '\nDate: ' + current_time + '\n')
    
    initial_text = 'Success: ' if status else 'Error: '
    file_object.write(initial_text + message)
    file_object.close()
    
def current_weather_data(location: str, key: str):
    '''
    Documentation at https://openweathermap.org/current

    location - 'City,Country', as 'Monterrey,Mx'
    key - api key
    '''
    http = requests.Session()
    assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
    http.hooks['response'] = [assert_status_hook]
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric'
    return  http.get(url)

def main():
    # Variables for the logger
    job_name = 'openweather'
    path = '/home/armando/Github Repos/weatherAPI_data_eng/src/'

    # Load Environment Variables
    try:
        config_object = ConfigParser(interpolation = None)
        config_object.read(path + 'config.ini')
    
        api_keys = config_object['API']    
        open_key = api_keys['open_weather_key']
        open_locs = api_keys['locations']

        influx_db = config_object['DATABASE']    
        my_token = influx_db['token']
        my_org = influx_db['organization']
        my_bucket = influx_db['bucket']

        logger(path, job_name, 'Env Variables Accesed', True)
    except Exception as e:
        logger(path, job_name, 'Env Variables Not Accessed, exit. ' + str(e), False)
        sys.exit(0)

    # Create a data point for each city in the list
    for open_loc in open_locs.split('/'):
        logger(path, job_name, 'City: '+ open_loc, True)

        # Connect to the API
        try:
            full_response = current_weather_data(open_loc, open_key)
            logger(path, job_name, 'Connected to the API', True)
        except Exception as e:
            # Hide the API key in the logs
            e = str(e).replace(open_key, 'hiden_key')
            logger(path, job_name, 'Not connecting to the API, exit. ' + str(e), False)
            continue

        # Normalize Json
        try:
            # Get the json with the data
            response_info = json.loads(full_response.text)
            # Normalize the json
            df_main_columns = pd.json_normalize(response_info) 
            # Normalize the weather column
            df_weather_columns = pd.json_normalize(response_info, record_path='weather').add_prefix('weather.')
            # Create 1 unique row of data
            df_final = pd.concat([df_main_columns, df_weather_columns], axis=1).drop(['weather'], axis=1)
            # Add a timestamp that humans can read
            df_final['dt_not_timezoned'] = pd.to_datetime(df_final['dt'], unit='s')
            logger(path, job_name, 'Normalizing Data', True)            
        except Exception as e:
            logger(path, job_name, 'Normalizing Data, exit. ' + str(e), False)
            continue

        # Store Data in influxdata.com
        try:
            json_body = [
                {
                    'measurement': 'weather',
                    'tags':
                    {
                        'country': df_final['sys.country'][0],
                        'city': df_final['name'][0],
                        'weather_class': df_final['weather.main'][0]
                    },
                    'time': df_final['dt_not_timezoned'][0].isoformat('T') + 'Z',
                    'fields': 
                    {
                        'visibility': df_final['visibility'][0],
                        'temperature': df_final['main.temp'][0],
                        'sensation': df_final['main.feels_like'][0],
                        'pressure': df_final['main.pressure'][0],
                        'humidity': df_final['main.humidity'][0],
                        'cloudiness': df_final['clouds.all'][0] 
                    }
                }
            ]

            with InfluxDBClient(url='https://us-east-1-1.aws.cloud2.influxdata.com', token=my_token, org=my_org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                write_api.write(my_bucket, my_org, json_body)
                client.close()
            logger(path, job_name, 'Storing the data', True)
        except Exception as e:
            logger(path, job_name, 'Storing the data, exit. ' + str(e), False)
            continue

if __name__ == '__main__':
    main()