import logging
logger = logging.getLogger('SHEETCLOUD DRIVE')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import io
import pandas as pd

from typing import *

from sheetcloud.conn import service



def list_my_csvs() -> List[Dict]:
    """ Returns a list of dict containing properties of all CSVs in the target account.
        Properties:
        - mimeType: str
        - parents (List of ids)
        - size 
        - id
        - name
        - modifiedTime
        - url

    Returns:
        List[Dict]: List of CSV properties
    """
    res = service('/drive/list/csv', method='post')
    if 'csvs' in res:
        logger.info(f'List contains a total of {len(res["csvs"])} CSVs.')
        return res['csvs']
    return list()


def read_csv(file_id: str) -> pd.DataFrame:
    """ Read a specific CSV file with ID `file_id`.

    Args:
        file_id (str): The id of the CSV file to read.

    Returns:
        pd.DataFrame: DataFrame containing the data of the CSV file.
    """
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/octet-stream',
    }
    params = {'file_id': file_id}
    content = service('/drive/read/csv', params=params, headers=headers, method='post', return_dict=False)
    df = pd.read_parquet(io.BytesIO(content), engine='pyarrow', use_nullable_dtypes=True)
    return df


def write_csv(name: str, df: pd.DataFrame) -> None:
    """ Write a pandas DataFrame to a CSV file with name `name` in the target account.

    Args:
        name (str): Name of the file (not ID)
        df (pd.DataFrame): DataFrame containing the data.
    """
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
        params = {'name': name}
        endpoint = '/drive/write/csv'
        _ = service(endpoint, params=params, files=files, method='post')
        




if __name__ == "__main__":
    print('Start connecting...')
    print(list_my_csvs())
    df = read_csv('1etL1yAilIh_mDuY7B_JH8sTY3Y0W3lKI')
    print(df)
    print(df.info())


    # df = pd.DataFrame([[1,2,3],[4,pd.NA,6],[7,7,pd.NA]], columns=['col1','col2','col3'])
    # df = pd.read_csv('../check.csv')
    # df = pd.concat([df, df, df, df], ignore_index=True) # ~2.8m entries (incl. NA)
    write_csv('sheetcloud-csv-test-1', df)

    print('Done')