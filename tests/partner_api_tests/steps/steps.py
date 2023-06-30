import requests
from behave import given, when, then

api_url = "http://localhost:8000/partners"


@given('a valid API key for Partner API')
def valid_api_key(context):
    context.api_key = "YOUR_API_KEY"  # Replace with your actual API key


@when('I create a partner with the following details:')
def create_partner(context):
    payload = context.table.rows[0].as_dict()
    response = requests.post(api_url, json=payload)
    context.response = response


@then('the response status code should be {status_code:d}')
def check_status_code(context, status_code):
    assert context.response.status_code == status_code, f"Expected status code {status_code}, but got {context.response.status_code}"


@then('the response should contain the following details:')
def check_response_details(context):
    expected_details = context.table.rows[0].as_dict()
    response_json = context.response.json()

    for field, value in expected_details.items():
        assert response_json[field] == value, f"Expected {field} to be {value}, but got {response_json[field]}"


@when('I read partners')
def read_partners(context):
    response = requests.get(api_url)
    context.response = response


@when('I read the nearest covering partner with longitude "{longitude}" and latitude "{latitude}"')
def read_nearest_covering_partner(context, longitude, latitude):
    query_params = {
        "long": longitude,
        "lat": latitude
    }
    response = requests.get(f"{api_url}/nearest", params=query_params)
    context.response = response
