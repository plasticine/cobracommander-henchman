import re, urlparse
from collections import defaultdict

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound

from lib import wsgi, logger
from views import socketio

class Server(wsgi.WSGIWebsocketBase):
    """
    BuildRelay runs a WSGI server and listens for connections over websockets.
    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)
        self.urls = Map([
            Rule('/', endpoint=root),
            Rule('/socket.io/<method>', endpoint=socketio.SocketIOHandler()),
        ])
        super(Server, self).__init__()

def root(request):
    return Response('hello from the builder server')

server = Server()
application = server.application

if __name__ == '__main__':
    from socketio import SocketIOServer
    SocketIOServer(('', 7000), application, resource="socket.io",
        policy_server=False).serve_forever()
