import logging
logger = logging.getLogger('SHEETCLOUD CONN')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import json
import time
import requests

from typing import *

from sheetcloud.utils import pw_obfuscator


ENV_SHEETCLOUD_API_URL = os.environ.get('SHEETCLOUD_API_URL', 'https://api.sheetcloud.de')
ENV_SHEETCLOUD_USERNAME = os.environ.get('SHEETCLOUD_USERNAME', 'missing')
ENV_SHEETCLOUD_PASSWORD = os.environ.get('SHEETCLOUD_PASSWORD', 'missing')
ENV_SHEETCLOUD_LICENSE = os.environ.get('SHEETCLOUD_LICENSE', None)


ENV_SHEETCLOUD_DEV = str(os.environ.get('SHEETCLOUD_DEV', 'False')).strip().lower() == 'true'
if ENV_SHEETCLOUD_DEV is not None:
    logger.debug(f'Development mode enabled. API is {ENV_SHEETCLOUD_API_URL}.')


logger.info(f'Environment variable SHEETCLOUD_USERNAME is {ENV_SHEETCLOUD_USERNAME}.')
logger.info(f'Environment variable SHEETCLOUD_PASSWORD is {pw_obfuscator(ENV_SHEETCLOUD_PASSWORD, "missing")}.')
if ENV_SHEETCLOUD_LICENSE is not None:
    logger.info(f'(Optional) Environment variable SHEETCLOUD_LICENSE is {pw_obfuscator(ENV_SHEETCLOUD_LICENSE, "missing")}.')

_sheetcloud_auth_token: str = None


class SheetcloudAuthorizationFailed(Exception):
    msg = """ Raised when authorization failed. Please check your user name and password as well as your internet connection. """
    def __str__(self) -> str:
        return self.msg



def service(path: str, data: Optional[Dict]=None, params: Optional[Dict]=None, files: Optional[Dict]=None, headers: Optional[Dict]=None, method: str='post', return_dict: bool=True, num_retries: int=3) -> Tuple[Dict, Any]:
    # normal request
    # curl -X 'GET'   'https://api.sheetcloud.de/sheets/list'   -H 'accept: application/json'   -H 'Authorization: Bearer johndoe    
    global _sheetcloud_auth_token
    if _sheetcloud_auth_token is None:
        logger.debug('Request authorization token.')
        auth_token = request_auth_token()
        if auth_token is None:
            raise SheetcloudAuthorizationFailed()
        _sheetcloud_auth_token = auth_token

    if headers is None:
        headers = {
            # 'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    headers['Authorization'] = f'Bearer {_sheetcloud_auth_token}'
    
    payload = None
    if data is not None:
        payload = json.dumps(data)

    while num_retries > 0:
        if method == 'post':
            response = requests.post(f'{ENV_SHEETCLOUD_API_URL}{path}', data=payload, params=params, files=files, headers=headers, timeout=100, verify=not ENV_SHEETCLOUD_DEV)
        else:
            response = requests.get(f'{ENV_SHEETCLOUD_API_URL}{path}', data=payload, params=params, files=files, headers=headers, timeout=100, verify=not ENV_SHEETCLOUD_DEV)

        if response.status_code in [401, 404]:
            logger.debug('Request new authorization token.')
            _sheetcloud_auth_token = request_auth_token()
            if _sheetcloud_auth_token is None:
                raise SheetcloudAuthorizationFailed()
            headers['Authorization'] = f'Bearer {_sheetcloud_auth_token}'
        if response.status_code == 200:
            break

        if files is not None:
            logger.debug(f'Manually setting seek(0) in case of re-tries.')
            files['file'][1].seek(0)
        time.sleep(3)
        num_retries -= 1

    if response.status_code != 200:
        logger.warning(f'Could not reach {path}.')
        if return_dict and response.content is not None:
            resp = response.json()
            logger.info(f'{resp}.')
        return dict()
    
    resp = dict()
    if return_dict and response.content is not None:
        resp = response.json()
    if not return_dict:
        resp = response.content
    return resp


def request_auth_token(num_retries: int=3) -> Optional[str]:
    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=&username={ENV_SHEETCLOUD_USERNAME}&password={ENV_SHEETCLOUD_PASSWORD}&scope=&client_id=&client_secret='
    while num_retries > 0:
        response = requests.post(f'{ENV_SHEETCLOUD_API_URL}/token', data, headers=headers, timeout=100, verify=not ENV_SHEETCLOUD_DEV)
        if response.status_code == 200:
            response_data_dict = response.json()
            access_token = response_data_dict['access_token']
            return access_token
        else:
            if response.status_code == 401:
                logger.error(f'Authorization failed. Check your user name and password again.')
                return None
            if response.content is not None:
                err_msg = response.json()
                if 'detail' in err_msg:
                    logger.error(f'Authorization failed with "{err_msg["detail"]}". Trying again...')
        time.sleep(3)
        num_retries -= 1
    logger.error(f'Authorization failed (user={ENV_SHEETCLOUD_USERNAME}, pw={pw_obfuscator(ENV_SHEETCLOUD_PASSWORD)}).')
    return None


if __name__ == "__main__":
    print('Start connecting...')
    token = request_auth_token()
    print(token)

    # webbrowser.open(f'{URL_SHEETCLOUD_API}login')
    print('Done')