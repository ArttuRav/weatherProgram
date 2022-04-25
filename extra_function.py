import config
import extra_function_data
from requests_ip_rotator import ApiGateway
import requests

def calls_exceeded(complete_url):
    gateway_url = 'http://api.openweathermap.org'
    gateway = ApiGateway(gateway_url, regions=['eu-west-1', 'eu-west-2'], access_key_id=config.aws_access_keyid, access_key_secret=config.aws_secret_access_key)
    gateway.start()

    session = requests.Session()
    session.mount(gateway_url, gateway)

    daily_response = session.get(complete_url)
    seven_day_data = daily_response.json()

    gateway.shutdown()

    extra_function_data.daily_data = seven_day_data
