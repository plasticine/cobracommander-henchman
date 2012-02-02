from gevent import monkey; monkey.patch_all()
import gevent_psycopg2; gevent_psycopg2.monkey_patch()

from optparse import OptionParser

from henchman import __version__, setup_environment
setup_environment()

from henchman.henchman import Henchman

if __name__ == '__main__':
    parser = OptionParser(version="%s" % (__version__))
    parser.add_option("-a", "--address", dest="address", help="hostname", default="localhost")
    parser.add_option("-p", "--port", dest="port", help="port", type="int", default=9000)
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="enable debugging", default=False)
    (options, args) = parser.parse_args()

    try:
        print """ _______                      __
|   |   |.-----..-----..----.|  |--..--------..---.-..-----.
|       ||  -__||     ||  __||     ||        ||  _  ||     |
|___|___||_____||__|__||____||__|__||__|__|__||___._||__|__|

Henchman is on patrol at http://%s:%s""" % (options.address, options.port)
        henchman = Henchman().run(options.address, options.port)
        print '-'*61
        print
        henchman.serve_forever()
    except KeyboardInterrupt, e:
        print "\nShutting down..."
        henchman.kill()
        print "Bye!"
