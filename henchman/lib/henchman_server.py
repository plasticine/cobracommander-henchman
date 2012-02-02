import os, re, urlparse
from collections import defaultdict

from werkzeug.wrappers import Request, Response

from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from socketio import SocketIOServer

import wsgi
from ..urls import urls

class HenchmanServer(wsgi.WSGIWebsocketBase):
    """
    HenchmanServer runs a WSGI server and listens for connections over websockets.
    """
    def __init__(self):
        self.urls = urls
        super(HenchmanServer, self).__init__()

    def run(self, address, port=9000):
        app = SharedDataMiddleware(self.application, {
            '/socket.io/socket.io.js': os.path.join(os.path.dirname(__file__), '../static/javascripts/socket.io.js'),
            '/static': os.path.join(os.path.dirname(__file__), '../static')
        })
        return SocketIOServer((address, port), app, resource="socket.io",
            policy_server=False)
