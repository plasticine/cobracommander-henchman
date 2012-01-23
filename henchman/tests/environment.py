from gevent.monkey import patch_all; patch_all()
import gevent
from multiprocessing import Process

from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection

from henchman import setup_environment
setup_environment()

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from henchman.lib.server import Server, run
from henchman.views.socketio import SocketIOHandler

interactive = True
verbosity = 0
old_name = settings.DATABASES['default']['NAME']

def before_all(context):
    setup_test_environment()

    # run the Henchman server
    # we need to wrap the serve_forever call in another process here to ensure
    # that it does not block the test execution yet is available to serve
    # testing requests.
    _server = Server()
    context.server = run(_server.application, 'localhost', 9999)
    context.process = Process(target=context.server.serve_forever)
    context.process.start()

    # create the werkzeug client wrapper
    context.client = Client(_server.application, BaseResponse)

def after_all(context):
    teardown_test_environment()

    # kill the server and shut down
    context.server.kill()
    context.process.terminate()

def before_scenario(context, scenario):
    # set up django database
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)

def after_scenario(context, scenario):
    # clean up django test DB
    connection.creation.destroy_test_db(old_name, verbosity)