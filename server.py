from optparse import OptionParser

from henchman import __version__, setup_environment
setup_environment()

from henchman.lib.server import Server, run

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
        server = Server()
        _henchman = run(server.application, options.address, options.port)
        _henchman.serve_forever()
        print '-'*61
        print
    except KeyboardInterrupt, e:
        print "\nShutting down..."
        _henchman.kill()
        print "Bye!"
