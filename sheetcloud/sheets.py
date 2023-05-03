import logging
logger = logging.getLogger('SHEETCLOUD SHEETS')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import io
import pandas as pd

from datetime import datetime
from typing import *

from sheetcloud.conn import service
from sheetcloud.templates import load_template


def list_my_spreadsheets() -> List[Dict]:
    res = service('/sheets/list', method='post')
    if 'sheets' in res:
        logger.info(f'List contains a total of {len(res["sheets"])} spreadsheets.')
        return res['sheets']
    return list()


def get_modified_datetime(sheet_url_or_name: str) -> datetime:
    res = service('/sheets/modified-time', params={'spreadsheet_url_or_name': sheet_url_or_name}, method='post')
    if 'timestamp' in res:
        return datetime.fromisoformat(res['timestamp'])
    logger.warning(f'Could not find timestamp of speadsheet {sheet_url_or_name}. Returning current time.')
    return datetime.now()


def format_spreadsheet(sheet_url_or_name: str, worksheet_name: str, a1range_format_list: List[Tuple[str, Dict]], auto_resize: bool=True) -> None:
    fmts = list()
    for e in a1range_format_list:
        print(e)
        fmts.append({'a1range': e[0], 'format': e[1]})
    print(fmts)
    params = {'spreadsheet_url_or_name': sheet_url_or_name, 'worksheet_name': worksheet_name, 'auto_resize': auto_resize}
    _ = service('/sheets/format', data={'formats': fmts}, params=params, method='post')


def share(sheet_url_or_name: str, share_emails_write_access: Optional[List[str]]=None, share_emails_read_only_access: Optional[List[str]]=None, notification_msg: Optional[str]=None) -> None:
    params = {'spreadsheet_url_or_name': sheet_url_or_name}
    data={'emails_write_access': share_emails_write_access, 'emails_read_access': share_emails_read_only_access, 'notification_msg': notification_msg}
    resp = service('/sheets/share', params=params, data=data)
    return resp


def read(sheet_url_or_name: str, worksheet_name: str, cache: bool=True) -> pd.DataFrame:
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/octet-stream',
    }
    params = {'spreadsheet_url_or_name': sheet_url_or_name, 'worksheet_name': worksheet_name}
    content = service('/sheets/read', params=params, headers=headers, method='post', return_dict=False)
    df = pd.read_parquet(io.BytesIO(content), engine='pyarrow', use_nullable_dtypes=True)
    print(df)
    return df


def write(sheet_url_or_name: str, worksheet_name: str, df: pd.DataFrame, append: bool=False, cache: bool=True) -> None:
    with io.BytesIO() as memory_buffer:
        df.to_parquet(
            memory_buffer,
            compression='gzip',
            engine='pyarrow'
        )
        memory_buffer.seek(0)
        # need to send files separately
        files = {
            'file': ('Test', memory_buffer, 'application/octet-stream')
        }
        params = {'spreadsheet_url_or_name': sheet_url_or_name, 'worksheet_name': worksheet_name}
        endpoint = '/sheets/append' if append else '/sheets/write'
        resp = service(endpoint, params=params, files=files, method='post')       


def append(sheet_url_or_name: str, worksheet_name: str, df: pd.DataFrame, cache: bool=True) -> None:
    write(sheet_url_or_name, worksheet_name, df, append=True, cache=cache)



if __name__ == "__main__":
    print('Start connecting...')
    # print(list_my_spreadsheets())
    # print(sheets)
    # read('sheetcloud-test', 'Sheet1')
    # print(get_modified_datetime('sheetcloud-test'))


    df = pd.DataFrame([[1,2,3],[4,pd.NA,6],[7,7,pd.NA]], columns=['col1','col2','col3'])
    # df = pd.read_csv('../check.csv')
    # df = pd.concat([df, df, df, df], ignore_index=True) # ~2.8m entries (incl. NA)
    # append('sheetcloud-test', 'write-test', df)
    # write('sheetcloud-test-1', 'write-test', df)
    # write('sheetcloud-test-2', 'write-test', df)
    # share('sheetcloud-test-1', share_emails_read_only_access=['nico.goernitz@gmail.com'], share_emails_write_access=['nico@morphais.com', 'abc@def.com'], notification_msg='Blubb blubb')

    # from sheetcloud.formats import data_small, header_red
    # format_spreadsheet('sheetcloud-test', 'write-test', [('A1:F1', header_red)], auto_resize=False)
    # format_spreadsheet('sheetcloud-test', 'write-test', [('A1:F1', header_red), ('A2:F10', data_small)], auto_resize=False)



    # webbrowser.open(f'{URL_SHEETCLOUD_API}login')
    print('Done')