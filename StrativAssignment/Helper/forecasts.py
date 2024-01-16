from ast import Param
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

retry_session = retry(retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"


def getForecasts(lat,long,start_date, end_date):
	params = {
		        "latitude": float(lat),
		        "longitude": float(long),
                "past_days":0,  
		        "start_hour":start_date,
		        "end_hour":end_date,
				
		        "hourly": "temperature_2m",
		        "utc_offset_seconds": 0,
		        "timezone": "Asia/Dhaka",   
		        "timezone_abbreviation": "asia"
	        }
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s"),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_dataframe = pd.DataFrame(data = hourly_data)

	return hourly_dataframe
