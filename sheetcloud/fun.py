import logging
logger = logging.getLogger('SHEETCLOUD FUN')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import pandas as pd

from typing import *

from sheetcloud import sheets
from sheetcloud import templates


def there_is_no_fun_here_yet():
    raise Exception('Ohhhhhh, no fun :(')

# def write_image(sheet_url_or_name: str, worksheet_name: str, img, cache: bool=True) -> None:

#     sheets.write(sheet_url_or_name, worksheet_name, df, cache=cache)

#     fmts = [('A:A', {'width': 250}), ('B:B', {'width': 500}), ('A1:B1', formats.header_blue), ('A2:A', formats.index_column_blue)]
#     sheets.format_spreadsheet(sheet_url_or_name, worksheet_name, a1range_format_list=fmts, auto_resize=False)



if __name__ == "__main__":
    print('Start connecting...')
    # do something here
    print('Done')