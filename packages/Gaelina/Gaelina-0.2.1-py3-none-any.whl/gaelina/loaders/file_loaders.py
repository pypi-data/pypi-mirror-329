import yaml

import toml
import hcl2 as hcl

from .utils import with_open, safe


@with_open
@safe(error_msg='Could not parse yaml')
def load_yaml(file_):
    docs = list(yaml.unsafe_load_all(file_))
    return docs[0] if len(docs) == 1 else docs


@with_open
@safe(error_msg='Could not parse HCL (v2)')
def load_hcl(file_):
    return hcl.load(file_)


@with_open
@safe(error_msg='Could not parse TOML')
def load_toml(file_):
    return toml.loads(file_.read())


@with_open
@safe(error_msg='Could not read', default_value='')
def load_str(file_):
    return file_.read()


@safe(error_msg='Could not parse list', default_value=[])
def load_lst(path):
    return load_str(path).strip().replace('\r', '').split('\n')
