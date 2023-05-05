from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

import pytest
import sheetcloud as sc


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


@pytest.fixture
def my_dc_list():
    sub_dc = MySubDC(my_sub_dcs1=[MySubSubDC(), MySubSubDC()])
    dc = MyDC(my_sub_dcs=[sub_dc, sub_dc]) 
    my_dcs = [dc, dc]
    yield my_dcs


@pytest.fixture
def my_classes():
    yield [MyDC, MySubDC, MySubSubDC]



def test_orm(my_dc_list, my_classes):
    sc.orm.write('sheetcloud-test', my_dc_list, 'ORM_TEST')
    objs = sc.orm.read('sheetcloud-test', 'ORM_TEST', my_classes)
    print(objs)
