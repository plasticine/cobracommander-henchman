import re, urlparse, os
from collections import defaultdict

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware

from lib import wsgi, logger
from views import static, socketio, minion

class Server(wsgi.WSGIWebsocketBase):
    """
    BuildRelay runs a WSGI server and listens for connections over websockets.
    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)
        self.urls = Map([
            Rule('/', endpoint=static.root),
            Rule('/minion', methods=['post'], endpoint=minion.spawn),
            Rule('/socket.io/<method>', endpoint=socketio.SocketIOHandler())
        ])
        super(Server, self).__init__()

server = Server()
application = server.application

if __name__ == '__main__':
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from henchman import __version__
    from socketio import SocketIOServer
    from optparse import OptionParser

    parser = OptionParser(version="%s" % (__version__))
    parser.add_option("-a", "--address", dest="address", help="hostname", default="localhost")
    parser.add_option("-p", "--port", dest="port", help="port", type="int", default=7000)
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="enable debugging", default=False)
    (options, args) = parser.parse_args()

    try:
        HOST = (options.address, options.port)
        print """ _______                      __
|   |   |.-----..-----..----.|  |--..--------..---.-..-----.
|       ||  -__||     ||  __||     ||        ||  _  ||     |
|___|___||_____||__|__||____||__|__||__|__|__||___._||__|__|

Henchman is on patrol at http://%s:%s""" % HOST
        application = SharedDataMiddleware(application, {
            '/socket.io/socket.io.js': os.path.join(os.path.dirname(__file__), 'static/javascripts/socket.io.js'),
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
        if options.debug:
            from werkzeug.debug import DebuggedApplication
            application = DebuggedApplication(application)
            print "Running with debugger enabled."
        print '-'*61
        print
        SocketIOServer(HOST, application, resource="socket.io",
            policy_server=False).serve_forever()
    except KeyboardInterrupt, e:
        print "\nShutting down..."
        socketio.SocketIOHandler.cleanup()
        print "Bye!"
