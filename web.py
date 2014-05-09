import os

from flask import Flask, request, Response
from flask.ext.cache import Cache
import requests


API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})


def append_args(path, args):
    '''Format query string (args) and append it to a URL path'''

    if len(request.args) == 0:
        return path

    params = ['%s=%s' % (key, args[key]) for key in args]
    query = '&'.join(params)
    return '%s?%s' % (path, query)


@cache.memoize(1)
def fetch(path, args={}):
    '''Fetch a url with optional query parameters and return a requests
    response'''

    path = append_args(path, args)
    headers = {
        'X-Mashape-Authorization': API_KEY
        }

    return requests.get(API_URL + path, headers=headers)


@app.route('/<path:path>')
def path_handler(path):

    r = fetch(path, request.args)

    print r.status_code, API_URL + path

    return Response(r.text, status=r.status_code,
                    content_type=r.headers['content-type'])


if __name__ == '__main__':
    app.run()
