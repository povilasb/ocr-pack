import os
import json
from typing import Union


def new_char_file(chars_dir: str='chars') -> str:
    chars = os.listdir(chars_dir)
    return '{}/{}.png'.format(chars_dir, len(chars) or 0)


def read_json_from(fname: str) -> Union[dict, list]:
    with open(fname, 'r') as f:
        return json.load(f)
