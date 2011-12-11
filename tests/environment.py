import gevent
from gevent.monkey import patch_all; patch_all()
from multiprocessing import Process
from ..server import server, run_server
from ..views.socketio import SocketIOHandler

def before_all(context):
    # run the Henchman server
    # we need to wrap the serve_forever call in another process here to ensure
    # that it does not block the test execution yet is available to serve
    # testing requests.
    context.server = run_server(server.application, 'localhost', 9999)
    context.process = Process(target=context.server.serve_forever)
    context.process.start()

def after_all(context):
    SocketIOHandler.cleanup()
    context.server.kill()
    context.process.terminate()
