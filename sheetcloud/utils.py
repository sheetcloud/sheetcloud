import logging
logger = logging.getLogger('SHEETCLOUD UTILS')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import os
import math
import json

from datetime import datetime, timezone
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
    obf = '******' if pw is None or len(pw) < 5 else f'{pw[:3]}****'
    if exception == pw:
        obf = pw
    return obf


def int2a1(number: int) -> str:
    out = ''
    while number >= 0:
        out = f'{chr(65 + (number % 26))}{out}'
        number = math.floor(number / 26) - 1
    return out
    

def get_modification_datetime_from_file(fname: str) -> Optional[datetime]:
    ts = None
    try:
        ts = datetime.fromtimestamp(os.path.getmtime(fname), timezone.utc)
    except BaseException as e:
        logger.info(f'Error while reading file {fname}.')
    return ts


def create_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


if __name__ == "__main__":
    print(int2a1(0))

    print(int2a1(20))
    print(int2a1(26))
    print(int2a1(27))

    print(int2a1(261))
    print(int2a1(26*26+25))
    print(int2a1(26*26+26))

    # create_dir('.tmp')