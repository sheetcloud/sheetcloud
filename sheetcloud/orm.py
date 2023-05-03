import logging
logger = logging.getLogger('SHEETCLOUD ORM')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import json
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


def build_dfs_from_dc_table(dc_table: List) -> Dict[str, pd.DataFrame]:
    df = pd.DataFrame.from_records(dc_table, columns=['parent', 'parent_class', 'parent_field', 'obj_class', 'obj', 'parent_uuid', 'obj_uuid'])
    
    table_names = df['parent_class'].unique().tolist()
    omit_vars = dict()
    for pc in table_names:
        omit_vars[pc] = df[df.parent_class == pc]['parent_field'].unique().tolist()
    print(omit_vars)

    tables = dict()
    for entry in dc_table:
        _, _, parent_field, obj_class, obj, parent_uuid, obj_uuid = entry

        od_org = asdict(obj)
        _ = [od_org.pop(ov, None) for ov in omit_vars.get(obj_class, list())]
        od = dict()
        for k, v in od_org.items():
            od[k] = json.dumps(v)
        od.update({'parent_uuid': str(parent_uuid) if parent_uuid is not None else None, 'uuid': str(obj_uuid), 'parent_field': parent_field})

        if not obj_class in tables: 
            tables[obj_class] = list()
        tables[obj_class].append(od)

    dfs = dict()
    for name, tbl in tables.items():
        dfs[name] = pd.DataFrame.from_dict(tbl)
    return dfs


def build_dc_table(dataclass_list: List, res_list: List, parent: Any, parent_field: str, parent_uuid: str) -> List:
    for dc in dataclass_list:
        if is_dataclass(dc):
            dc_uuid = uuid.uuid4()
            parent_class = None if parent is None else type(parent).__name__
            res_list.append( (parent, parent_class, parent_field, type(dc).__name__, dc, parent_uuid, dc_uuid) )

            for f in fields(dc):
                if isinstance(vars(dc)[f.name], list):
                    res_list = build_dc_table(vars(dc)[f.name], res_list, dc, f.name, dc_uuid)
                # asdict(dataclass_list[0])  
    return res_list


def write(sheet_url_or_name: str, dataclass_list: List, prefix: str='orm', template_name: Optional[str]=None, cache: bool=True) -> None:
    dc_table = build_dc_table(dataclass_list, list(), parent=None, parent_field=None, parent_uuid=None)
    dfs = build_dfs_from_dc_table(dc_table)

    for tbl_name, tbl_df in dfs.items():
        worksheet_name = f'{prefix}_{tbl_name}'
        sheets.write(sheet_url_or_name, worksheet_name, tbl_df, cache=cache)  


if __name__ == "__main__":
    print('Start connecting...')
    
    sub_dc = MySubDC(my_sub_dcs1=[MySubSubDC(), MySubSubDC()])
    dc = MyDC(my_sub_dcs=[sub_dc, sub_dc]) 
    my_dcs = [dc, dc]

    write('sheetcloud-test', my_dcs)

    print('Done')