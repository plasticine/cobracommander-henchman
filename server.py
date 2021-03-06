#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent_psycopg2; gevent_psycopg2.monkey_patch()

from optparse import OptionParser
from termcolor import colored

from henchman import __version__, setup_environment
setup_environment()

from henchman.henchman import Henchman

if __name__ == '__main__':
    parser = OptionParser(version="%s" % (__version__))
    parser.add_option("-a", "--address", dest="address", help="hostname", default="localhost")
    parser.add_option("-p", "--port", dest="port", help="port", type="int", default=9000)
    (options, args) = parser.parse_args()

    try:
        print colored(""" _______                      __
|   |   |.-----..-----..----.|  |--..--------..---.-..-----.
|       ||  -__||     ||  __||     ||        ||  _  ||     |
|___|___||_____||__|__||____||__|__||__|__|__||___._||__|__|

Henchman v%s is on patrol at http://%s:%s""" % (__version__, options.address, options.port), 'blue')
        print colored('-'*60, 'blue')
        print
        henchman = Henchman().run(options.address, options.port)
        henchman.serve_forever()
    except KeyboardInterrupt, e:
        print colored("\nShutting down...", 'red')
        henchman.kill()
        print "Bye!"
