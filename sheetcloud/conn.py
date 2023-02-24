import logging
logger = logging.getLogger('SHEETCLOUD')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import json
import time
import requests
import webbrowser

import pandas as pd

from typing import *

from sheetcloud.utils import load_endpoint_config, pw_obfuscator

SHEETCLOUD_API_URL = 'https://api.sheetcloud.de'

ENV_SHEETCLOUD_USERNAME = os.environ.get('SHEETCLOUD_USERNAME', 'env-sheetcloud-username-not-found')
ENV_SHEETCLOUD_PASSWORD = os.environ.get('SHEETCLOUD_PASSWORD', 'env-sheetcloud-password-not-found')


class _SheetCloudV1():
    base_url: str = SHEETCLOUD_API_URL
    username: str = ENV_SHEETCLOUD_USERNAME
    password: str = ENV_SHEETCLOUD_PASSWORD
    
    _endpoints: Dict | None = None
    _auth_token: str | None = None

    def __init__(self) -> None:
        self._endpoints = load_endpoint_config('v1')
        self._auth_token = self._request_auth_token()

    def list_spreadsheets(self) -> List:
        res = self._communicate(self._endpoints['data']['list_spreadsheets'])
        if 'sheets' in res:
            logger.warning('Return')
            logger.info(res['sheets'])
            return res['sheets']
        logger.warning('Empty response.')
        return list()

    def read_worksheet(self, sheet_id: str, worksheet_name: str):
        res = self._communicate(f"{self._endpoints['data']['read_worksheet']}/{sheet_id}/{worksheet_name}")
        if 'data' in res:
            logger.warning('Return')
            logger.info(res['data'])
            data = res['data']
            print(data)
            df = pd.DataFrame.from_records(data)
            print(df)
            return df
        logger.warning('Empty response.')
        return list()

    def write_worksheet(self, sheet_id: str, worksheet_name: str, df: pd.DataFrame):
        df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['c1','c2','c3'])
        print(df)
        data = json.loads(df.to_json(orient='records'))
        print(data)
        res = self._communicate(f"{self._endpoints['data']['write_worksheet']}/{sheet_id}/{worksheet_name}", data)
        print(res)
        return res

    def _communicate(self, path: str, data: Dict | None=None, num_retries: int=3):
        # normal request
        # curl -X 'GET'   'https://api.sheetcloud.de/sheets/list'   -H 'accept: application/json'   -H 'Authorization: Bearer johndoe    
        headers = {
            'accept': 'application/json', 
            'Authorization': f'Bearer {self._auth_token}'
        }
        payload = None
        if data is not None:
            payload = json.dumps(data)
        while num_retries > 0:
            response = requests.get(f'{self.base_url}{path}', payload, headers=headers, timeout=100)
            print(response)
            if response.status_code in [401, 404]:
                logger.debug('Request new authorization token.')
                self._auth_token = self._request_auth_token()
                headers = {
                    'accept': 'application/json', 
                    'Authorization': f'Bearer {self._auth_token}'
                }
            if response.status_code == 200:
                break
            time.sleep(3)
            num_retries -= 1
        if response.status_code != 200:
            logger.warning(f'Could not reach {path}.')
        resp = {}
        if response.content is not None:
            resp = response.json()
            print('data: ', resp)
        return resp

    def _request_auth_token(self, num_retries: int=3) -> str:
        headers = {
            'accept': 'application/json', 
            'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={self.username}&password={self.password}&scope=&client_id=&client_secret='
        while num_retries > 0:
            response = requests.post(f'{self.base_url}{self._endpoints["auth"]}', data, headers=headers, timeout=100)            
            if response.status_code == 200:
                response_data_dict = response.json()
                access_token = response_data_dict['access_token']
                return access_token
            else:
                if response.content is not None:
                    err_msg = response.json()
                    if 'detail' in err_msg:
                        logger.error(f'Authorization failed with "{err_msg["detail"]}". Trying again...')
            time.sleep(3)
            num_retries -= 1
        logger.error(f'Authorization failed (user={self.username}, pw={pw_obfuscator(self.password)}).')
        return 'authorization-failed'


class SheetCloudMeta(type):
    @property
    def v1(cls) -> _SheetCloudV1:
        cls._v1 = _SheetCloudV1()
        return cls._v1


class SheetCloud(metaclass=SheetCloudMeta):
    _v1: _SheetCloudV1 | None = None


if __name__ == "__main__":
    print('Start connecting...')
    # SheetCloud.v1.list_spreadsheets()
    # SheetCloud.v1.read_worksheet('flow_test_sheet', 'Sheet1')
    SheetCloud.v1.write_worksheet('flow_test_sheet', 'Sheet1', None)
    # webbrowser.open(f'{URL_SHEETCLOUD_API}login')
    print('Done')