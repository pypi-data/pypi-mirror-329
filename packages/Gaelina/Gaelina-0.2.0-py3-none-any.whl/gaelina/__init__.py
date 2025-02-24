import jinja2

from .loaders import load_any, load_filters
from .exceptions import GaelinaRenderingException

MAX_ITERATIONS = 200


def gaelina(path):
    source = Source(path)
    if isinstance(source.data, dict):
        return GaelinaDict(source.data, source)
    return source.data


def gaelina_value(value, source):
    if isinstance(value, dict):
        return GaelinaDict(value, source)
    if isinstance(value, list):
        return GaelinaList(value, source)
    if isinstance(value, str) and '{{' in value:
        return g_render(value, source)
    return value


def g_render(str_, source):
    render = str_
    for _ in range(MAX_ITERATIONS):
        new_render = source.render(render)
        if new_render == render:
            return render
        if not isinstance(new_render, str):
            return gaelina_value(new_render, source)
        render = new_render
    raise GaelinaRenderingException(f'Failed to render template: {str_}')


class Source:
    def __init__(self, path):
        self.data = gaelina_value(load_any(path), self)
        self.filters = load_filters(path, self.data)
        self.env = jinja2.Environment() # nosec
        for filter_name, filter_ in self.filters.items():
            self.env.filters[filter_name] = filter_
        if isinstance(self.data, dict):
            self.data = {k: gaelina_value(v, self) for k, v in self.data.items()}

    def consider_a_value(self, str_):
        return str_.startswith('{{') and str_.endswith('}}') and '{{' not in str_[2:]

    def render(self, str_):
        if self.consider_a_value(str_):
            expression = str_[2:-2].strip()
            return self.env.compile_expression(expression)(**self.data)

        # Somehow trailing line feed are removed by jinja2 readding them
        trail = '\n' if str_.endswith('\n') else ''

        return self.env.from_string(str_).render(**self.data) + trail


class GaelinaDict(dict):
    def __init__(self, value, source):
        super().__init__(value)
        self.source = source

    def __getitem__(self, key):
        value = super().__getitem__(key)
        return gaelina_value(value, self.source)

    def get(self, key, default_value):
        value = super().get(key, default_value)
        return gaelina_value(value, self.source)

    def values(self):
        return tuple(
            gaelina_value(v, self.source)
            for _, v in super().items()
        )

    def items(self):
        return tuple(
            (k, gaelina_value(v, self.source))
            for k, v in super().items()
        )


class GaelinaList(list):
    def __init__(self, value, source):
        super().__init__(value)
        self.source = source

    def __getitem__(self, index):
        value = super().__getitem__(index)
        if isinstance(index, slice):
            return GaelinaList(value, self.source)
        return gaelina_value(value, self.source)
