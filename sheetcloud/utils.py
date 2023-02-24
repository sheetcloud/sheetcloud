import json

from typing import Dict


def load_endpoint_config(version_name: str) -> Dict:
    data = {}
    fp = open(f'resources/endpoints.{version_name}.json')
    data = json.load(fp)
    return data


def pw_obfuscator(pw: str) -> str:
    return '******' if len(pw) < 5 else f'{pw[:3]}****'
