from typing import Dict


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


header_grey = {
    "backgroundColor": {
        "red": 0.9,
        "green": 0.9,
        "blue": 0.9
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
    "fontSize": 11,
    "bold": True
    }
}        


header_red = {
    "padding": {
        "top": 10,
        "right": 10,
        "bottom": 4,
        "left": 3
    },
    "borders": {
        "top": {
            "style": FORMAT_BORDER_STYLE_SOLID_THICK,
            "color": {
                "red": 0.9,
                "green": 0.2,
                "blue": 0.8
            },
        },
        "bottom": {
            "style": FORMAT_BORDER_STYLE_DASHED,
            "color": {
                "red": 0.9,
                "green": 0.2,
                "blue": 0.8,
            },
        },
    #   "left": {
    #     object (Border)
    #   },
    #   "right": {
    #     object (Border)
    #   }
    },
    "backgroundColor": {
        "red": 0.9,
        "green": 0.6,
        "blue": 0.6,
    },
    "horizontalAlignment": FORMAT_HORIZONTAL_ALIGN_CENTER,
    "verticalAlignment": FORMAT_VERTICAL_ALIGN_MIDDLE,
    "wrapStrategy": FORMAT_TEXT_WRAP_CLIP,
    "textFormat": {
        "foregroundColorStyle": {
            "rgbColor": {
                "red": 0.6,
                "green": 0.0,
                "blue": 0.2,
                "alpha": 1.0
            }
        },
        "fontSize": 10,
        "bold": True,
        "italic": False,
        "strikethrough": False,
        "underline": False,
    },
    "textRotation": {
        "angle": -30,
        # "vertical": False  # use either .. or ..
    },
    "width": 200,
    "height": 50
}        


data_small = {
    "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
    },
    "horizontalAlignment": "RIGHT",
    "textFormat": {
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
    "fontSize": 8,
    "bold": False
    }
}        


data_med = {
    "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
    },
    "horizontalAlignment": "RIGHT",
    "textFormat": {
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
    "fontSize": 10,
    "bold": False
    }
}        


def build() -> Dict:
    pass