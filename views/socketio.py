import gevent
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

from lib import logger
from lib.socketio.channel import SocketIOChannelProxy
# from lib.socketio import events

CLIENTS = {}

class SocketIOHandler(object):
    """

    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)

    def __call__(self, server, request, method):
        """"""
        # wrap up the socket.io object in SocketIOChannelProxy to add channels
        socket = SocketIOChannelProxy(request.environ["socketio"])

        print dir(socket)

        # store the request and socket objects in the client dict
        CLIENTS[socket.session.session_id] = (request, socket)



        # try:
        #     while True:
        #         # wait for messages
        #         message = socket.recv()
        #         if len(message):
        #             if message[0] == '__subscribe__' and len(message) == 2:
        #                 # subscribe the socket to the channel
        #                 self.logger.info("__subscribe__ %s on %s", socket, message[1])
        #                 socket.subscribe(message[1])
        #                 # events.on_subscribe.send(request, socket, channel=message[1])
        #             elif message[0] == '__unsubscribe__' and len(message) == 2:
        #                 # unsubscribe the socket from channel
        #                 self.logger.info("%__unsubscribe__ %s on %s", socket, message[1])
        #                 socket.unsubscribe(message[1])
        #                 # events.on_unsubscribe.send(request, socket, channel=message[1])
        #             else:
        #                 for client in CLIENTS:
        #                     client.socket.send('test')
        #                 # handle regular messages
        #                 # events.on_message.send(request, socket, message)
        #                 pass
        #         elif not socket.connected():
        #             self.logger.info("%s disconnected %s", socket)
        #             # events.on_disconnect.send(request, socket)
        #             break
        # except Exception, e:
        #     raise e
        # del CLIENTS[socket.session.session_id]
        return Response('hello')
