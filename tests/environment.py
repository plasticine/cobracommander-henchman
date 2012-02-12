from gevent.monkey import patch_all; patch_all()
import gevent
import os
from multiprocessing import Process

from django import db
from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command

from henchman import setup_environment
setup_environment()

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from henchman.henchman import Henchman
from henchman.views.socketio import SocketIOHandler

old_name = settings.DATABASES['default']['NAME']

def before_all(context):
    setup_test_environment()
    context.fixture_path = lambda * x: os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'fixtures', *x)
    )

def after_all(context):
    # clean up django test DB
    try:
        db.close_connection()
        db.connection.creation.destroy_test_db(old_name, verbosity=0)
    except Exception, e:
        pass
    teardown_test_environment()

def before_feature(context, feature):
    if 'db' in feature.tags:
        # set up django database
        db.connection.creation.create_test_db(
            verbosity=0,
            autoclobber=False
        )
        db.connection.enter_transaction_management()

    if 'browser' in feature.tags:
        # run the Henchman server
        # we need to wrap the serve_forever call in another process here to ensure
        # that it does not block the test execution yet is available to serve
        # testing requests.
        context.henchman = Henchman()
        context.server = context.henchman.run('localhost', 9999)
        context.process = Process(target=context.server.serve_forever)
        context.process.start()
        # create the werkzeug client wrapper
        context.client = Client(context.henchman.application, BaseResponse)

def after_feature(context, feature):
    if 'db' in feature.tags:
        # truncate the database between each feature
        call_command(
            'flush',
            verbosity=1,
            interactive=False,
            database=db.connection.alias
        )

    if 'browser' in feature.tags:
        # kill the server and shut down
        context.process.terminate()

def before_scenario(context, scenario):
    # start transaction management for the db conenction
    if 'db' in scenario.feature.tags:
        db.transaction.enter_transaction_management(managed=True)
        db.transaction.managed(True)

def after_scenario(context, scenario):
    # rollback transactions and end transaction management
    if 'db' in scenario.feature.tags:
        db.transaction.rollback()
        db.transaction.leave_transaction_management()
