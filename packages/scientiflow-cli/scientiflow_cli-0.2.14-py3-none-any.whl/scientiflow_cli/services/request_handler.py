import requests
from scientiflow_cli.config import Config
from scientiflow_cli.cli.auth_utils import getAuthToken

app_base_url = Config.APP_BASE_URL


def handle_response(response, error_message):
    if response.status_code == 200:
        return response
    else:
        if error_message:
          raise Exception(f"ERROR with status code {response.status_code}: {error_message}")
        else:
          raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

def make_auth_request(endpoint,method,data=None,params=None,error_message=None):
    headers = {'Authorization': f'Bearer {getAuthToken()}'}
    try:
        if method == 'GET':
            response = requests.get(app_base_url+endpoint,headers=headers,params=params)
        elif method == 'POST':
            response = requests.post(app_base_url+endpoint, json=data,headers=headers)
        return handle_response(response, error_message)
    except requests.RequestException as e:
        return "Unsupported HTTP method"
    
def make_no_auth_request(endpoint,method,data=None,error_message=None):
    try:
        if method == 'GET':
                response = requests.get(app_base_url+endpoint)
        elif method == 'POST':
                response = requests.post(app_base_url+endpoint, json=data)
        return handle_response(response, error_message)
    except requests.RequestException as e:
        return "Unsupported HTTP method"
    