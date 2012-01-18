from gevent.monkey import patch_all; patch_all()
import gevent
from multiprocessing import Process

from henchman import setup_environment
setup_environment()

from henchman.lib.server import Server, run
from henchman.views.socketio import SocketIOHandler

def before_all(context):
    # run the Henchman server
    # we need to wrap the serve_forever call in another process here to ensure
    # that it does not block the test execution yet is available to serve
    # testing requests.
    _server = Server()
    context.server = run(_server.application, 'localhost', 9999)
    context.process = Process(target=context.server.serve_forever)
    context.process.start()

def after_all(context):
    context.server.kill()
    context.process.terminate()
