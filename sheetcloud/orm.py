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


def get_fully_qualified_classname(obj) -> str:
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def _build_object(class_name: str, content: Dict, name_to_class: Dict) -> Any:
    obj = None
    my_cls = name_to_class.get(class_name, None)
    if my_cls is not None:
        decoded_params = dict()
        for k, v in content.items():
            if v is not None:
                decoded_params[k] = json.loads(v)
            else:
                decoded_params[k] = None
        obj = my_cls(**decoded_params)
    return obj


def read(sheet_url_or_name: str, prefix_id: str, classes: List[Any], cache: bool=True) -> Optional[List]:
    res = None
    try:
        res = _build_dc_list_from_sheets(sheet_url_or_name=sheet_url_or_name, prefix_id=prefix_id, classes=classes, cache=cache)
    except BaseException as e:
        logger.error(f'There was a problem loading {prefix_id} worksheets from {sheet_url_or_name} and building the list of dataclasses. Please double check the inputs and consult the documentation in order to not run into limitations.')
    return res


def _build_dc_list_from_sheets(sheet_url_or_name: str, prefix_id: str, classes: List[Any], cache: bool=True) -> Optional[List]:
    name_to_class = dict()
    for c in classes:
        name_to_class[c.__name__] = c

    names = sheets.list_worksheets_in_spreadsheet(sheet_url_or_name)

    query_by_uuid = dict()
    query_by_parent_uuuid_and_field = dict()
    for s in names:
        if str(s).startswith(prefix_id):
            class_name = str(s).removeprefix(f'{prefix_id}_')
            df = sheets.read(sheet_url_or_name, s, cache=cache)

            for i in range(df.shape[0]):
                content = df.iloc[i].to_dict()
                uuid = content.pop('uuid', None)
                parent_uuid = content.pop('parent_uuid', None)
                parent_field = content.pop('parent_field', None)
                parent_class = content.pop('parent_class', None)
        
                obj = _build_object(class_name, content, name_to_class)
        
                query_by_uuid[uuid] = obj
                if parent_uuid not in query_by_parent_uuuid_and_field:
                    query_by_parent_uuuid_and_field[parent_uuid] = dict()
                if parent_field not in query_by_parent_uuuid_and_field[parent_uuid]:
                    query_by_parent_uuuid_and_field[parent_uuid][parent_field] = list()
                query_by_parent_uuuid_and_field[parent_uuid][parent_field].append(obj)

    obj_list = list()
    for uuid, fields in query_by_parent_uuuid_and_field.items():
        parent = query_by_uuid.get(uuid, None)
        if parent is None and None in fields:
            obj_list.extend(fields[None])
        else:
            for f, f_list in fields.items():
                parent.__setattr__(f, f_list)

    return obj_list


def _build_dfs_from_dc_table(dc_table: List) -> Dict[str, pd.DataFrame]:
    df = pd.DataFrame.from_records(dc_table, columns=['parent', 'parent_class', 'parent_field', 'obj_class', 'obj', 'parent_uuid', 'obj_uuid'])
    
    table_names = df['parent_class'].unique().tolist()
    omit_vars = dict()
    for pc in table_names:
        omit_vars[pc] = df[df.parent_class == pc]['parent_field'].unique().tolist()
    print(omit_vars)

    tables = dict()
    for entry in dc_table:
        parent, parent_class, parent_field, obj_class, obj, parent_uuid, obj_uuid = entry

        od_org = asdict(obj)
        _ = [od_org.pop(ov, None) for ov in omit_vars.get(obj_class, list())]
        od = dict()
        for k, v in od_org.items():
            if v is None:
                od[k] = None
            else:
                od[k] = json.dumps(v)

        # parent_class = get_fully_qualified_classname(parent)
        od.update({'uuid': str(obj_uuid), 'parent_uuid': str(parent_uuid) if parent_uuid is not None else None, 'parent_class': parent_class, 'parent_field': parent_field})

        if not obj_class in tables: 
            tables[obj_class] = list()
        tables[obj_class].append(od)

    dfs = dict()
    for name, tbl in tables.items():
        dfs[name] = pd.DataFrame.from_dict(tbl)
    return dfs


def _build_dc_table(dataclass_list: List, res_list: List, parent: Any, parent_field: str, parent_uuid: str) -> List:
    for dc in dataclass_list:
        if is_dataclass(dc):
            dc_uuid = uuid.uuid4()
            parent_class = None if parent is None else type(parent).__name__
            res_list.append( (parent, parent_class, parent_field, type(dc).__name__, dc, parent_uuid, dc_uuid) )

            for f in fields(dc):
                if isinstance(vars(dc)[f.name], list):
                    res_list = _build_dc_table(vars(dc)[f.name], res_list, dc, f.name, dc_uuid)
    return res_list


def write(sheet_url_or_name: str, dataclass_list: List, prefix_id: str, cache: bool=True) -> None:
    dc_table = _build_dc_table(dataclass_list, list(), parent=None, parent_field=None, parent_uuid=None)
    try:
        dfs = _build_dfs_from_dc_table(dc_table)
    except BaseException as e:
        logging.error(f'Error while encoding dataclasses. Please consult the documentation to ensure not running into limitations.')
        return None

    for tbl_name, tbl_df in dfs.items():
        worksheet_name = f'{prefix_id}_{tbl_name}'
        sheets.write(sheet_url_or_name, worksheet_name, tbl_df, cache=cache)  


if __name__ == "__main__":
    print('Start connecting...')
    
    print('Done')