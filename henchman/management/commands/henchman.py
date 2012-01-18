# from gevent import monkey; monkey.patch_all()
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        print "test"
        # from henchman import __version__, setup_environment
        # setup_environment()
        # from henchman.lib.server import Server, run
        # server = Server()
        # _henchman = run(server.application, options.address, options.port)
        # _henchman.serve_forever()
