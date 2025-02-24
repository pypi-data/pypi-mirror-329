import os

from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec


def load_filters(path, context):
    module = load_filter_module(f'{path}/filters.py')
    filters = getattr(module, 'get_filters', lambda _: {})(context)
    if len(filters) == 0:
        print('No filters loaded.')
    return filters


def load_filter_module(path):
    if not os.path.exists(path):
        print('No filters file found.')
        return None

    module_name = 'custom_filters'
    loader = SourceFileLoader(module_name, path)
    spec = spec_from_loader(module_name, loader)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
