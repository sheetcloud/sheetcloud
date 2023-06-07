import logging
logger = logging.getLogger('SHEETCLOUD SHEETS')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import io
import pandas as pd

from datetime import datetime, timezone
from typing import *

from sheetcloud.conn import service, ENV_SHEETCLOUD_DEV
from sheetcloud.utils import get_modification_datetime_from_file, create_dir
from sheetcloud.templates import load_template

if not ENV_SHEETCLOUD_DEV:
    import warnings
    warnings.filterwarnings("ignore")

SHEETCLOUD_CACHE_PATH = '.tmp'



def list_spreadsheets() -> List[Dict]:
    res = service('/sheets/list', method='post')
    if 'sheets' in res:
        logger.info(f'List contains a total of {len(res["sheets"])} spreadsheets.')
        return res['sheets']
    return list()


def list_worksheets_in_spreadsheet(sheet_url_or_name: str) -> List[str]:
    res = service('/sheets/list', method='post', params={'spreadsheet_url_or_name': sheet_url_or_name})
    if 'sheets' in res:
        logger.info(f'List contains a total of {len(res["sheets"])} worksheets.')
        return res['sheets']
    return list()


def get_modified_datetime(sheet_url_or_name: str) -> Tuple[datetime, str, str]:
    res = service('/sheets/modified-time', params={'spreadsheet_url_or_name': sheet_url_or_name}, method='post')
    if 'timestamp' in res:
        ts = datetime.fromisoformat(res['timestamp'])
        ts = ts.astimezone(timezone.utc)
        return ts, res['id'], res['title']
    logger.warning(f'Could not find timestamp of speadsheet {sheet_url_or_name}. Returning current time.')
    return datetime.now(), None, None


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


def _cache_read(id: str, worksheet: str, ts: datetime) -> Optional[pd.DataFrame]:
    create_dir(SHEETCLOUD_CACHE_PATH)
    fname = f'{SHEETCLOUD_CACHE_PATH}/{id}_{worksheet}.parquet'
    ts_local = get_modification_datetime_from_file(fname)
    if ts_local is not None and ts_local < ts:
        logger.debug(f'Restore {worksheet} from local cache. Local ts={ts_local}, remote ts={ts}.')
        return pd.read_parquet(fname)
    return None


def _cache_write(id: str, worksheet: str, df: pd.DataFrame, append: bool, ts: datetime) -> None:
    create_dir(SHEETCLOUD_CACHE_PATH)
    fname = f'{SHEETCLOUD_CACHE_PATH}/{id}_{worksheet}.parquet'
    if not append:
        df.to_parquet(fname)
        ts_local = get_modification_datetime_from_file(fname)
        logger.debug(f'Store worksheet {worksheet} in local cache. Local ts={ts_local}, remote ts={ts}.')
    else:
        ts_local = get_modification_datetime_from_file(fname)
        logger.debug(f'Checking if data can be appended to worksheet {worksheet} in local cache. Local ts={ts_local}, remote ts={ts}.')
        if ts_local is not None and ts_local < ts:
            df_org = pd.read_parquet(fname)
            df = pd.concat([df_org, df], ignore_index=True)
            df.to_parquet(fname)
            ts_local = get_modification_datetime_from_file(fname)
            logger.debug(f'Appending data to worksheet {worksheet} in local cache. Local ts={ts_local}, remote ts={ts}.')


def infer_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        c_num = pd.to_numeric(df[c], errors='ignore')
        c_dt = pd.to_datetime(df[c], errors='ignore', infer_datetime_format=True)

        if c_dt.dtype == 'object' and not c_num.dtype == 'object': 
            df[c] = c_num
        if not c_dt.dtype == 'object' and c_num.dtype == 'object': 
            df[c] = c_dt
    return df


def read(sheet_url_or_name: str, worksheet_name: str, try_infer_dtypes: bool=True, cache: bool=True) -> pd.DataFrame:
    """ Read worksheet from spreadsheet into a DataFrame.

    Args:
        sheet_url_or_name (str): The name or URL of an spreadsheet
        worksheet_name (str): The worksheet name
        try_infer_dtypes (bool, optional): Dtypes such as float/int need to be inferred otherwise dtype will be object. Defaults to True.
        cache (bool, optional): Caching large amounts of read-only data locally is much faster when accessing it multiple times. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame containing the data of `worksheet_name` of spreadsheet `sheet_url_or_name`
    """
    ts = None
    id = None
    if cache:
        ts, id, title = get_modified_datetime(sheet_url_or_name)
        if id is not None:
            df = _cache_read(id=id, worksheet=worksheet_name, ts=ts)
            if df is not None:
                return df

    # no cached version available
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/octet-stream',
    }
    params = {'spreadsheet_url_or_name': sheet_url_or_name, 'worksheet_name': worksheet_name}
    content = service('/sheets/read', params=params, headers=headers, method='post', return_dict=False)
    df = pd.read_parquet(io.BytesIO(content), engine='pyarrow', use_nullable_dtypes=True)
    if cache and id is not None:
        _cache_write(id, worksheet_name, df, False, ts)

    if try_infer_dtypes:
        df = infer_dtypes(df)
    return df


def write(sheet_url_or_name: str, worksheet_name: str, df: pd.DataFrame, append: bool=False, cache: bool=True) -> None:
    """ Write a DataFrame to a specific worksheet within a given spreadsheet. If no spreadsheet with the given name exists, create a 
        new one. Same holds true for a worksheet. Beware: if a the worksheet contains data. 

    Args:
        sheet_url_or_name (str): The name or URL of an spreadsheet
        worksheet_name (str): The worksheet name
        df (pd.DataFrame): Data to store.
        append (bool, optional): Append the data instead of overwrite. Assumes the worksheet exists. Defaults to False.
        cache (bool, optional): Caching large amounts of read-only data locally is much faster when accessing it multiple times. Defaults to True.
    """
    # make dates json serializable
    dfc = df.select_dtypes(include=['datetime', 'datetimetz'])
    df[dfc.columns] = dfc.astype('str')
    
    if cache:
        ts, id, title = get_modified_datetime(sheet_url_or_name)
        if id is not None:
            _cache_write(id=id, worksheet=worksheet_name, df=df, append=append, ts=ts)

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
    # print(list_spreadsheets())
    # print(list_worksheets_in_spreadsheet('sheetcloud-test'))

    # print(sheets)
    # df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    # df['a_date_time'] = datetime.now()
    # df['an_int_column'] = 10
    # print(df.info())
    # write('sheetcloud-test', 'write-test', df)

    df = read('sheetcloud-test', 'write-test')

    print(df.info())
    # print(get_modified_datetime('sheetcloud-test'))


    df = pd.DataFrame([[1,2,3],[4,pd.NA,6],[7,7,pd.NA]], columns=['col1','col2','col3'])
    # df = pd.read_csv('../check.csv')
    # df = pd.concat([df, df, df, df], ignore_index=True) # ~2.8m entries (incl. NA)
    # append('sheetcloud-test', 'write-test', df)
    # write('sheetcloud-test', 'write-test', df)
    # write('sheetcloud-test-2', 'write-test', df)
    # share('sheetcloud-test-1', share_emails_read_only_access=['nico.goernitz@gmail.com'], share_emails_write_access=['nico@morphais.com', 'abc@def.com'], notification_msg='Blubb blubb')

    # from sheetcloud.formats import data_small, header_red
    # format_spreadsheet('sheetcloud-test', 'write-test', [('A1:F1', header_red)], auto_resize=False)
    # format_spreadsheet('sheetcloud-test', 'write-test', [('A1:F1', header_red), ('A2:F10', data_small)], auto_resize=False)



    # webbrowser.open(f'{URL_SHEETCLOUD_API}login')
    print('Done')