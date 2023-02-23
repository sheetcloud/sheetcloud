import json
import time
import requests

URL_SHEETCLOUD_API = 'https://api.sheetcloud.de/'

PATH_SHEETCLOUD_AUTH = 'token'
PATH_SHEETCLOUD_LIST = 'sheets/list'


def communicate(path: str, token: str, data: str):
   # normal request
   # curl -X 'GET'   'https://api.sheetcloud.de/sheets/list'   -H 'accept: application/json'   -H 'Authorization: Bearer johndoe    
    num_tries = 3
    status = 0
    headers = {
        'accept': 'application/json', 
        'Authorization': f'Bearer {token}'
    }
    payload = json.dumps(data)
    while num_tries>0:
        response = requests.get(f'{URL_SHEETCLOUD_API}{path}', payload, headers=headers, timeout=100)
        print(response)
        if response.status_code == 200:
            break
        time.sleep(3)
        num_tries -= 1
    assert response.status_code == 200
    print(response)
    resp = response.json()
    print('data: ', resp)


def get_token(username: str, password: str):
    num_tries = 3
    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=&username={username}&password={password}&scope=&client_id=&client_secret='
    while num_tries > 0:
        response = requests.post(f'{URL_SHEETCLOUD_API}{PATH_SHEETCLOUD_AUTH}', data, headers=headers, timeout=100)
        if response.status_code == 200:
            response_data_dict = response.json()
            token_type = response_data_dict['token_type']
            access_token = response_data_dict['access_token']
            return access_token
        time.sleep(3)
        num_tries -= 1
    print('Authorization failed.')
    return 'authorization-failed'


if __name__ == "__main__":
    print('Start connecting...')
    token = get_token('johndoe', 'secret')
    communicate(PATH_SHEETCLOUD_LIST, token, None)
    print('Done')