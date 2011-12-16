import os, re, urlparse
from collections import defaultdict

from socketio import SocketIOServer
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware

import wsgi, logger, buildqueue
from ..views import static, socketio, builds

class Server(wsgi.WSGIWebsocketBase):
    """
    BuildRelay runs a WSGI server and listens for connections over websockets.
    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)
        self.queue = buildqueue.BuildQueue()
        self.urls = Map([
            Rule('/', endpoint=static.root),
            Rule('/builds/new', methods=['post'], endpoint=builds.new),
            Rule('/socket.io/<method>', endpoint=socketio.SocketIOHandler())
        ])
        super(Server, self).__init__()

def run(app, address, port):
    app = SharedDataMiddleware(app, {
        '/socket.io/socket.io.js': os.path.join(os.path.dirname(__file__), '../static/javascripts/socket.io.js'),
        '/static': os.path.join(os.path.dirname(__file__), '../static')
    })
    return SocketIOServer((address, port), app, resource="socket.io",
        policy_server=False)