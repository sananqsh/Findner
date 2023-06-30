import os
from dotenv import load_dotenv

import requests
from behave import given, when, then
import time

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

@given('a valid API key for OpenWeatherMap API')
def valid_api_key(context):
    context.api_key = API_KEY

@when('I send a GET request to retrieve weather information for "{city}"')
def send_get_request(context, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={context.api_key}"
    response = requests.get(url)
    context.response = response

@then('the response status code should be {status_code:d}')
def check_status_code(context, status_code):
    assert context.response.status_code == status_code, f"Expected status code {status_code}, but got {context.response.status_code}"

@then('the response should contain the weather information for "{city}"')
def check_weather_info(context, city):
    response_data = context.response.json()
    assert response_data["name"] == city, f"Expected response for {city}, but got response for {response_data['name']}"

@when('I send a GET request to retrieve weather information for an invalid city')
def send_get_request(context):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=InvalidCity&appid={context.api_key}"
    response = requests.get(url)
    context.response = response


@when('I send a GET request to retrieve weather information for "{city}" with optional parameters')
def send_get_request_with_options(context, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={context.api_key}&units=metric&lang=en"
    response = requests.get(url)
    context.response = response

@then('the response should contain the weather information based on the specified parameters')
def check_weather_info_with_options(context):
    response_data = context.response.json()
    assert "main" in response_data, "Weather 'main' information not found in the response"
    assert "weather" in response_data, "Weather 'weather' information not found in the response"
    assert "wind" in response_data, "Weather 'wind' information not found in the response"
    assert "sys" in response_data, "Weather 'sys' information not found in the response"

@when('I send multiple GET requests within a short time frame')
def send_multiple_requests(context):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={context.api_key}"
    response_list = []
    for _ in range(5):
        response = requests.get(url)
        response_list.append(response)
        time.sleep(1)
    context.responses = response_list

@then('the response status code should indicate rate limiting exceeded')
def check_rate_limiting(context):
    for response in context.responses:
        assert response.status_code == 429, "Expected status code 429 for rate limiting exceeded"
