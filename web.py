import os

from flask import Flask, Markup, redirect, render_template, request, Response
import requests


app = Flask(__name__)
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')


def append_args(path, args):
    params = ['%s=%s' % (key, args[key]) for key in args]
    query = '&'.join(params)
    return '%s?%s' % (path, query)


@app.route('/<path:path>')
def path_handler(path):

    if len(request.args) > 0:
        path = append_args(path, request.args)

    headers = {
        'X-Mashape-Authorization': API_KEY
        }

    r = requests.get(API_URL + path, headers=headers)

    return Response(r.text, status=r.status_code,
                    content_type=r.headers['content-type'])


if __name__ == '__main__':
    app.run()
