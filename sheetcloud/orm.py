import logging
logger = logging.getLogger('SHEETCLOUD ORM')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import uuid
import pandas as pd

from typing import *
from dataclasses import is_dataclass, dataclass, asdict, fields, field


from sheetcloud import sheets
from sheetcloud import templates


@dataclass
class MySubSubDC:
    name: str = 'myname'


@dataclass
class MySubDC:
    another_float: float=3.1415
    my_sub_dcs1: Optional[List[MySubSubDC]] = None
    my_sub_dcs2: Optional[List[MySubSubDC]] = None


@dataclass
class MyDC:
    my_int: int = 2
    my_str: str = 'my_str'
    my_list_int: List[int] = field(default_factory=lambda: [1,2,3,4])
    my_dict: Dict[str, Any] = field(default_factory=lambda: {'key1': 'value1', 'key2': 'value2'})
    my_sub_dcs: Optional[List[MySubDC]] = None


# def read(sheet_url_or_name: str, worksheet_name: str, export: bool=True, cache: bool=True) -> Optional[Dict[str, str]]:
#     df = sheets.read(sheet_url_or_name, worksheet_name, cache=cache)
#     ud = dict(zip(df[df.columns[0]], df[df.columns[1]]))
#     if export:
#         logger.info(f'Adding {len(ud)} variables to the environment.')
#         for k, v in ud.items():
#             os.environ[k] = v
#     return ud


def build_df_from_dcs(dataclass_list: List) -> pd.DataFrame:
    for dc in dataclass_list:
        if is_dataclass(dc):
            print(asdict(dataclass_list[0]))
        else:
            logger.warning(f'Not a dataclass {str(dc)}.')


def build_dc_table(dataclass_list: List, res_list: List, parent: Any, parent_field: str) -> List:
    for dc in dataclass_list:
        if is_dataclass(dc):
            res_list.append( (parent, parent_field, dc, uuid.uuid4()) )

            for f in fields(dc):
                if isinstance(vars(dc)[f.name], list):
                    res_list = build_dc_table(vars(dc)[f.name], res_list, dc, f.name)
                # asdict(dataclass_list[0])  
    return res_list


def write(sheet_url_or_name: str, dataclass_list: List, prefix: str='orm_', cache: bool=True) -> None:

    dc_list = build_dc_table(dataclass_list, list(), parent=None, parent_field=None)

    df = pd.DataFrame.from_records(dc_list)

    print('\n\n')
    print(df)
    # print(dc_list)
    # df = pd.DataFrame.from_records([env])
    # df = df.transpose()
    # df.reset_index(inplace=True)
    # df.rename(columns={'index': 'key', 0: 'value'}, inplace=True)
    # print(df)
    # logger.info(f'Writing {df.shape[0]} env variables to worksheet {worksheet_name} in spreadsheet {sheet_url_or_name}.')
    # sheets.write(sheet_url_or_name, worksheet_name, df, cache=cache)



if __name__ == "__main__":
    print('Start connecting...')
    
    sub_dc = MySubDC(my_sub_dcs1=[MySubSubDC(), MySubSubDC()])
    dc = MyDC(my_sub_dcs=[sub_dc, sub_dc]) 
    my_dcs = [dc, dc]

    write('sheetcloud-test', my_dcs)

    print('Done')