import sys
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound
from django_socketio import events
from django_socketio.channels import SocketIOChannelProxy

from ..lib import logger

CLIENTS = {}
class SocketIOHandler(object):
    """

    """
    def __init__(self):
        self.logger = logger.get_logger(__name__)

    @staticmethod
    def cleanup():
        """
        Sends the on_finish signal to any open clients when the server
        is unexpectedly stopped.
        """
        for (request, socket, context) in CLIENTS.values():
            events.on_finish.send(request, socket, context)

    def __call__(self, server, request, method):
        context = {}
        socket = SocketIOChannelProxy(request.environ["socketio"])
        CLIENTS[socket.session.session_id] = (request, socket, context)

        try:
            if socket.on_connect():
                events.on_connect.send(request, socket, context)
            while True:
                message = socket.recv()
                if len(message) > 0:
                    if message[0] == '__subscribe__' and len(message) == 2:
                        self.logger.info('__subscribe__ socket %s to channel %s',
                            socket.session.session_id,  message[1])
                        socket.subscribe(message[1])
                        events.on_subscribe.send(request, socket, context, message[1])
                    elif message[0] == '__unsubscribe__' and len(message) == 2:
                        self.logger.info('__unsubscribe__ socket %s from channel %s',
                            socket.session.session_id,  message[1])
                        events.on_unsubscribe.send(request, socket, context, message[1])
                        socket.unsubscribe(message[1])
                    else:
                        events.on_message.send(request, socket, context, message)
                else:
                    if not socket.connected():
                        events.on_disconnect.send(request, socket, context)
                        break
        except Exception, e:
            events.on_error.send(request, socket, context, e)
            raise e

        events.on_finish.send(request, socket, context)
        del CLIENTS[socket.session.session_id]
        return Response("")
