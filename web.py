import os

from flask import Flask, request, Response
import requests


API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')
app = Flask(__name__)


def append_args(path, args):
    '''Format query string (args) and append it to a URL path'''

    if len(request.args) == 0:
        return path

    params = ['%s=%s' % (key, args[key]) for key in args]
    query = '&'.join(params)
    return '%s?%s' % (path, query)


@app.route('/<path:path>')
def path_handler(path):

    path = append_args(path, request.args)

    headers = {
        'X-Mashape-Authorization': API_KEY
        }

    r = requests.get(API_URL + path, headers=headers)

    print r.status_code, API_URL + path

    return Response(r.text, status=r.status_code,
                    content_type=r.headers['content-type'])


if __name__ == '__main__':
    app.run()
