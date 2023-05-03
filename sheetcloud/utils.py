import logging
logger = logging.getLogger('SHEETCLOUD UTILS')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import math
import json

from typing import Dict, Optional


def load_json(fname: str) -> Optional[Dict]:
    fname = fname.strip()
    if not fname.lower().endswith('.json'):
        fname = f'{fname}.json'
    data = None
    try:
        fp = open(f'resources/{fname}')
        data = json.load(fp)
    except BaseException as e:
        logger.warning(f'Could not load {fname}.')
    return data


def load_endpoint_config(version_name: str) -> Dict:
    return load_json(f'resources/endpoints.{version_name}.json')


def pw_obfuscator(pw: str, exception: str=None) -> str:
    obf = '******' if len(pw) < 5 else f'{pw[:3]}****'
    if exception == pw:
        obf = pw
    return obf


def int2a1(number: int) -> str:
    out = ''
    while number >= 0:
        out = f'{chr(65 + (number % 26))}{out}'
        number = math.floor(number / 26) - 1
    return out
    


if __name__ == "__main__":
    print(int2a1(0))

    print(int2a1(20))
    print(int2a1(26))
    print(int2a1(27))

    print(int2a1(261))
    print(int2a1(26*26+25))
    print(int2a1(26*26+26))
