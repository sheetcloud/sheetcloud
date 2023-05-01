import math
import json

from typing import Dict


def load_endpoint_config(version_name: str) -> Dict:
    data = {}
    fp = open(f'resources/endpoints.{version_name}.json')
    data = json.load(fp)
    return data


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
