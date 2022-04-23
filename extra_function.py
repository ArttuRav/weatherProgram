import config
from requests_ip_rotator import ApiGateway
import requests

def calls_exceeded(complete_url):
    api_key = config.api_key_backup

    gateway_url = 'http://api.openweathermap.org'
    gateway = ApiGateway(gateway_url, regions=['eu-west-1', 'eu-west-2'], access_key_id=config.aws_access_keyid, access_key_secret=config.aws_secret_access_key)
    gateway.start()

    session = requests.Session()
    session.mount(gateway_url, gateway)

    daily_response = session.get(complete_url)
    daily_data = daily_response.json()

    # print(daily_data)

    gateway.shutdown()

    return daily_data