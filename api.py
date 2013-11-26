from bottle import default_app
from bottle import route, request, response, get, post, put, abort, hook

import library_api
import racing_api

@route('/')
def hello_world():
    return 'API experiments'

application = default_app()


