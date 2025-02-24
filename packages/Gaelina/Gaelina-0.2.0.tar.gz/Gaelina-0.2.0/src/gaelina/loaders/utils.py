import traceback


def safe(error_msg='Could not load', default_value=None):
    def wrapper(function):
        def _(path):
            try:
                return function(path)
            except: # pylint: disable=bare-except
                print(f'[ERROR] {error_msg}: {path}')
                traceback.print_exc()
                return default_value
        return _
    return wrapper


def with_open(function):
    def wrapped(path):
        with open(path, 'r', encoding='utf-8') as file_:
            return function(file_)
    return wrapped


def path_to_name(path):
    return path.split('/')[-1].split('.')[0]
