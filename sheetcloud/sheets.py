import logging
logger = logging.getLogger('SHEETCLOUD.SHEETS')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import io
import os
import json
import time
import requests

import pandas as pd

from typing import *

from sheetcloud.utils import load_endpoint_config, pw_obfuscator


ENV_SHEETCLOUD_USERNAME = os.environ.get('SHEETCLOUD_USERNAME', 'env-sheetcloud-username-not-found')
ENV_SHEETCLOUD_PASSWORD = os.environ.get('SHEETCLOUD_PASSWORD', 'env-sheetcloud-password-not-found')
ENV_SHEETCLOUD_LICENSE = os.environ.get('SHEETCLOUD_LICENSE', 'env-sheetcloud-license-not-found')
ENV_SHEETCLOUD_TOKEN = os.environ.get('SHEETCLOUD_TOKEN', 'env-sheetcloud-token-not-found')

ENV_SHEETCLOUD_DEV = os.environ.get('SHEETCLOUD_DEV', False)


if ENV_SHEETCLOUD_DEV:
    SHEETCLOUD_API_URL = 'https://localhost:8080'
else:
    SHEETCLOUD_API_URL = 'https://api.sheetcloud.de'


class SheetcloudAuthorizationFailed(Exception):
    msg = """ Raised when authorization failed. Please check your user name and password as well as your internet connection. """
    def __str__(self) -> str:
        return self.msg


class _Sheets():
    base_url: str = SHEETCLOUD_API_URL
    username: str = ENV_SHEETCLOUD_USERNAME
    password: str = ENV_SHEETCLOUD_PASSWORD
    
    _endpoints: Dict | None = None
    _auth_token: str | None = None

    def __init__(self) -> None:
        self._endpoints = load_endpoint_config('v1')
        self._auth_token = self._request_auth_token()

    def list(self) -> List:
        res = self._communicate(self._endpoints['data']['list_spreadsheets'])
        if 'sheets' in res:
            logger.warning('Return')
            logger.info(res['sheets'])
            return res['sheets']
        logger.warning('Empty response.')
        return list()

    def read(self, sheet_id: str, worksheet_name: str):
        # headers for request
        headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/octet-stream',
                'Authorization': f'Bearer {self._auth_token}'
        }
        resp = requests.post(f"{SHEETCLOUD_API_URL}{self._endpoints['data']['read_worksheet']}/{sheet_id}/{worksheet_name}", headers=headers, verify=not ENV_SHEETCLOUD_DEV)
        status_code = resp.status_code
        print(status_code)
        df = pd.read_parquet(io.BytesIO(resp.content), engine='pyarrow', use_nullable_dtypes=True)

        print(df)
        return df

    def write(self, sheet_id: str, worksheet_name: str, df: pd.DataFrame):
        print(df)
        # data = json.loads(df.to_json(orient='records'))
        # print(data)
        # res = self._communicate(f"{self._endpoints['data']['write_worksheet']}/{sheet_id}/{worksheet_name}", data)
        # print(res)

        with io.BytesIO() as memory_buffer:
            df.to_parquet(
                memory_buffer,
                compression='gzip',
                engine='pyarrow'
            )
            memory_buffer.seek(0)
            # need to encode parameters as json string
            data = dict()
            headers = {
                'accept': 'application/json', 
                'Authorization': f'Bearer {self._auth_token}'
            }

            # need to send files separately
            files = {
                'file': ('Test', memory_buffer, 'application/octet-stream')
            }
            resp = requests.post(f'https://localhost:8080/sheets/write/{sheet_id}/{worksheet_name}', 
                                headers=headers, data=data, files=files, verify=not ENV_SHEETCLOUD_DEV)
            print(resp)


        return resp

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
            response = requests.get(f'{self.base_url}{path}', payload, headers=headers, timeout=100, verify=not ENV_SHEETCLOUD_DEV)
            # print(response)
            if response.status_code in [401, 404]:
                logger.debug('Request new authorization token.')
                self._auth_token = self._request_auth_token()
                if self._auth_token is None:
                    raise SheetcloudAuthorizationFailed()
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

    def _request_auth_token(self, num_retries: int=3) -> str | None:
        headers = {
            'accept': 'application/json', 
            'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={self.username}&password={self.password}&scope=&client_id=&client_secret='
        while num_retries > 0:
            response = requests.post(f'{self.base_url}{self._endpoints["auth"]}', data, headers=headers, timeout=100, verify=not ENV_SHEETCLOUD_DEV)
            if response.status_code == 200:
                response_data_dict = response.json()
                access_token = response_data_dict['access_token']
                print('Access Token=', access_token)
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
        logger.error(f'Authorization failed (user={self.username}, pw={pw_obfuscator(self.password)}).')
        return None


class SheetCloudMeta(type):
    @property
    def sheets(cls) -> _Sheets:
        cls._sheets = _Sheets()
        return cls._sheets


class SheetCloud(metaclass=SheetCloudMeta):
    _sheets: Union[_Sheets, None] = None


if __name__ == "__main__":
    print('Start connecting...')
    SheetCloud.sheets.list()
    # SheetCloud.data.read_worksheet('flow_test_sheet', 'Sheet12')

    # df = pd.DataFrame([[1,2,3],[4,pd.NA,6],[7,7,pd.NA]], columns=['col1','col2','col3'])
    # df = pd.read_csv('/home/nicococo/Documents/check.csv')
    # SheetCloud.data.write_worksheet('flow_test_sheet', 'Sheet1', df)

    # webbrowser.open(f'{URL_SHEETCLOUD_API}login')
    print('Done')