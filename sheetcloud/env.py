import logging
logger = logging.getLogger('SHEETCLOUD ENV')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import pandas as pd

from typing import *

from sheetcloud import sheets
from sheetcloud import templates


def read(sheet_url_or_name: str, worksheet_name: str, export: bool=True, cache: bool=True) -> Optional[Dict[str, str]]:
    df = sheets.read(sheet_url_or_name, worksheet_name, cache=cache)
    ud = dict(zip(df[df.columns[0]], df[df.columns[1]]))
    if export:
        logger.info(f'Adding {len(ud)} variables to the environment.')
        for k, v in ud.items():
            os.environ[k] = v
    return ud


def write(sheet_url_or_name: str, worksheet_name: str, env: Dict[str, str], template_name: Optional[str]='red_sailfish', cache: bool=True) -> None:
    df = pd.DataFrame.from_records([env])
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'key', 0: 'value'}, inplace=True)
    print(df)
    logger.info(f'Writing {df.shape[0]} env variables to worksheet {worksheet_name} in spreadsheet {sheet_url_or_name}.')
    sheets.write(sheet_url_or_name, worksheet_name, df, cache=cache)

    if template_name is not None:
        tmp = templates.load_template(template_name)
        fmts = tmp.apply(df, highlight_columns=['A'], ws=[('A', 250), ('B', 500)])
        # fmts = [tmp.empty.build('A:A', w=250), tmp.empty.build('B:B', w=500), tmp.header.build('A1:B1'), tmp.highlight_column.build('A2:A')]
        sheets.format_spreadsheet(sheet_url_or_name, worksheet_name, a1range_format_list=fmts, auto_resize=tmp.auto_resize)



if __name__ == "__main__":
    print('Start connecting...')
    env = read('sheetcloud-test', 'env')
    print(env)

    env.update({'ANOTHER_VAR': 'blopp'})
    write('sheetcloud-test', 'env2', env)

    print('Done')