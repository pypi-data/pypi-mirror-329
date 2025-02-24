import os
import copy

from ..exceptions import GaelinaUnmergeableException
from .file_loader import load_file
from .utils import path_to_name

ELEMENTS_TO_IGNORE = '.git', 'filters.py', '__pycache__'


def load_any(path):
    return load_dir(path) if os.path.isdir(path) else load_file(path)


def load_dir(dir_path):
    data = None
    for dir_element_path in os.listdir(dir_path):
        if dir_element_path in ELEMENTS_TO_IGNORE:
            continue
        sub_data = load_any(dir_path + '/' + dir_element_path)
        if dir_element_path.startswith('_'):
            data = merged_data(data, sub_data)
        else:
            data = merged_data(data, {path_to_name(dir_element_path): sub_data})
    return data


def merged_data(d1, d2):
    if d1 is None and d2 is not None:
        return d2
    type_match = (type(d1), type(d2))
    if type_match == (list, list):
        return d1 + d2
    if type_match == (dict, dict):
        return merged_dicts(d1, d2)
    raise GaelinaUnmergeableException(f'Unmergeable data {d1} and {d2}.')


def merged_dicts(d1, *dicts):
    res = copy.deepcopy(d1 or {})
    for d2 in dicts:
        rec_add_dict(res, d2 or {}, [])
    return res


def rec_add_dict(dest, src, path):
    for k, v in src.items():
        if k not in dest:
            dest[k] = copy.deepcopy(v)
        else:
            type_match = (type(dest[k]), type(v))
            if type_match == (list, list):
                dest[k] += v
            elif type_match == (dict, dict):
                rec_add_dict(dest[k], v, path + [k])
            else:
                raise GaelinaUnmergeableException(f'Trying to replace existing value for key {k} at {" -> ".join(path)}.')
