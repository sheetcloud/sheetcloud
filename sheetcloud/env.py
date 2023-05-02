import logging
logger = logging.getLogger('SHEETCLOUD ENV')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import pandas as pd

from typing import *

from sheetcloud import sheets
from sheetcloud import formats


def read(sheet_url_or_name: str, worksheet_name: str, export: bool=True, cache: bool=True) -> Optional[Dict[str, str]]:
    df = sheets.read(sheet_url_or_name, worksheet_name, cache=cache)
    ud = dict(zip(df[df.columns[0]], df[df.columns[1]]))
    if export:
        logger.info(f'Adding {len(ud)} variables to the environment.')
        for k, v in ud.items():
            os.environ[k] = v
    return ud


def write(sheet_url_or_name: str, worksheet_name: str, env: Dict[str, str], cache: bool=True) -> None:
    df = pd.DataFrame.from_records([env])
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'key', 0: 'value'}, inplace=True)
    print(df)
    logger.info(f'Writing {df.shape[0]} env variables to worksheet {worksheet_name} in spreadsheet {sheet_url_or_name}.')
    sheets.write(sheet_url_or_name, worksheet_name, df, cache=cache)

    fmts = [('A:A', {'wrapStrategy': formats.FORMAT_TEXT_WRAP_CLIP, 'width': 250}), ('B:B', {'wrapStrategy': formats.FORMAT_TEXT_WRAP_CLIP, 'width': 500}), ('A1:B1', formats.header_blue), ('A2:A', formats.index_column_blue)]
    # fmts = [('A1:B1', formats.header_blue), ('A2:A', formats.index_column_blue)]
    sheets.format_spreadsheet(sheet_url_or_name, worksheet_name, a1range_format_list=fmts, auto_resize=False)



if __name__ == "__main__":
    print('Start connecting...')
    env = read('sheetcloud-test', 'env')
    print(env)

    env.update({'ANOTHER_VAR': 'blopp'})
    write('sheetcloud-test', 'env2', env)

    print('Done')