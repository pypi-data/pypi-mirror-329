import os

from .file_loaders import load_yaml, load_str, load_lst, load_hcl, load_toml
from .special_loaders import load_x

EXT_TO_LOADER = {
    'yml': load_yaml,
    'yaml': load_yaml,
    'json': load_yaml,
    'text': load_str,
    'txt': load_str,
    '': load_str,
    'lst': load_lst,
    'hcl': load_hcl,
    'toml': load_toml,
    'tml': load_toml,
    'x': load_x,
}


def load_file(path):
    if not os.path.exists(path):
        print(f'[ERROR] {path} not found, ignored...')
        return {}

    ext = path.split('.')[-1] if '.' in path else ''

    return EXT_TO_LOADER.get(ext, load_str)(path)
