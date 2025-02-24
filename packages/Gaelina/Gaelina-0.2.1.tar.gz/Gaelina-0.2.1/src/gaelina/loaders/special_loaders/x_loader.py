import requests

from ..utils import safe


API_URL = 'https://publish.twitter.com/oembed'


class Xception(Exception):
    pass


@safe(error_msg='Could not load X file')
def load_x(path):
    with open(path, 'r', encoding='utf-8') as file_:
        lines = [line for line in file_.read().split('\n') if line]
        if len(lines) > 3:
            raise Xception('X file has too many lines (>2)')
        if len(lines) == 0:
            raise Xception('Empty X file')
        if len(lines) == 2:
            return {'link': lines[0], 'embedded': lines[1]}

    embedded = get_embedded_tweet(lines[0])
    update_x_file(path, lines[0], embedded)

    return {'link': lines[0], 'embedded': embedded}


def get_embedded_tweet(tweet_link):
    response = requests.get(API_URL, params={'url': tweet_link, 'omit_script': 'false'}, timeout=30)
    return response.json()['html']


def update_x_file(path, link, embedded):
    with open(path, 'w', encoding='utf-8') as file_:
        file_.write(f'{link}\n{embedded}')
