import logging
logger = logging.getLogger('SHEETCLOUD TEMPLATES')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import pandas as pd

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List

from sheetcloud.utils import load_json, int2a1


FORMAT_BORDER_STYLE_DOTTED = 'DOTTED' 	# The border is dotted.
FORMAT_BORDER_STYLE_DASHED = 'DASHED' 	# The border is dashed.
FORMAT_BORDER_STYLE_SOLID = 'SOLID' 	# The border is a thin solid line.
FORMAT_BORDER_STYLE_SOLID_MEDIUM = 'SOLID_MEDIUM' 	# The border is a medium solid line.
FORMAT_BORDER_STYLE_SOLID_THICK = 'SOLID_THICK' 	# The border is a thick solid line.
FORMAT_BORDER_STYLE_NONE = 'NONE' 	# No border. Used only when updating a border in order to erase it.
FORMAT_BORDER_STYLE_DOUBLE = 'DOUBLE' 	#  The border is two solid lines. 

FORMAT_HORIZONTAL_ALIGN_CENTER = 'CENTER'
FORMAT_HORIZONTAL_ALIGN_LEFT = 'LEFT'
FORMAT_HORIZONTAL_ALIGN_RIGHT = 'RIGHT'

FORMAT_VERTICAL_ALIGN_MIDDLE = 'MIDDLE'
FORMAT_VERTICAL_ALIGN_TOP = 'TOP'
FORMAT_VERTICAL_ALIGN_BOTTOM = 'BOTTOM'

FORMAT_TEXT_WRAP_OVERFLOW = 'OVERFLOW_CELL'
FORMAT_TEXT_WRAP_CLIP = 'CLIP'
FORMAT_TEXT_WRAP_WRAP = 'WRAP'


class SheetcloudTemplateDict(Dict):
    def build(self, a1range: str, w: int=-1, h: int=-1) -> Tuple[str, Dict]:
        ret = dict(self)
        if w >= 0:
            ret['width'] = w
        if h >= 0:
            ret['height'] = h
        return (a1range, ret)


class SheetcloudTemplate():
    name: str
    header: SheetcloudTemplateDict
    body: SheetcloudTemplateDict
    highlight_column: SheetcloudTemplateDict
    empty: SheetcloudTemplateDict
    auto_resize: bool=False
    def __init__(self, name: str, template: Dict, auto_resize: bool=False) -> None:
        self.name = name
        self.header = SheetcloudTemplateDict(template['header'])
        self.body = SheetcloudTemplateDict(template['body'])
        self.highlight_column = SheetcloudTemplateDict(template['highlight_column'])
        self.empty = SheetcloudTemplateDict(dict())
        self.auto_resize = auto_resize

    def apply(self, df: pd.DataFrame, highlight_columns: Optional[List[str]]=None, ws: Optional[List[Tuple[str, int]]]=None) -> List[Tuple[str, Dict]]:
        rows, cols = df.shape
        a1_cols_end = int2a1(cols-1)
        res = list()

        # header
        res.append(self.header.build(f'A1:{a1_cols_end}1'))
        # body
        res.append(self.body.build(f'A2:{a1_cols_end}{rows+1}'))
        # highlight columns
        if highlight_columns is not None:
            for hc in highlight_columns:
                res.append(self.highlight_column.build(f'{hc}2:{hc}{rows+1}'))
        # widths
        if ws is not None:
            for c, w in ws:
                res.append(self.empty.build(f'{c}:{c}', w=w))
        return res


def load_template(name: str) -> Optional[SheetcloudTemplate]:
    name = name.strip().lower()
    template = load_json(f'template_{name}.json')
    if template is None:
        logger.warning(f'Could not find template with name {name}.')
    else:
        template = SheetcloudTemplate(name, template)
    return template


# header_red = {
#     "padding": {
#         "top": 10,
#         "right": 10,
#         "bottom": 4,
#         "left": 3
#     },
#     "textRotation": {
#         "angle": -30,
#         # "vertical": False  # use either .. or ..
#     },
#     "width": 200,
#     "height": 50
# }        


if __name__ == "__main__":
    print('Start templates...')
    template = load_template('blue_sailfish')
    print(template)

    print(template.header.build('A1:B1', h=10))
    template.body.build('abc')

    print('Done')