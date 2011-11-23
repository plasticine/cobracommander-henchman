import re, urlparse
from collections import defaultdict

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound

from lib import wsgi, logger
from views import static, socketio

class Server(wsgi.WSGIWebsocketBase):
    """
    BuildRelay runs a WSGI server and listens for connections over websockets.
    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)
        self.urls = Map([
            Rule('/', endpoint=static.root),
            Rule('/socket.io/<method>', endpoint=socketio.SocketIOHandler()),
        ])
        super(Server, self).__init__()

server = Server()
application = server.application

if __name__ == '__main__':
    HOST = ('localhost', 7000)
    from socketio import SocketIOServer
    try:
        print """ _______                      __
|   |   |.-----..-----..----.|  |--..--------..---.-..-----.
|       ||  -__||     ||  __||     ||        ||  _  ||     |
|___|___||_____||__|__||____||__|__||__|__|__||___._||__|__|

Henchman is on patrol at http://%s:%s
""" % HOST
        SocketIOServer(HOST, application, resource="socket.io",
        policy_server=False).serve_forever()
    except KeyboardInterrupt, e:
        print "\nShutting down..."
