import gevent
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

from lib.socketio.channel import SocketIOChannelProxy
from lib.socketio import events

CLIENTS = {}

class SocketIOHandler(object):
    """

    """

    def __call__(self, server, request, method):
        """"""
        # wrap up the socket.io object in SocketIOChannelProxy to add channels
        socket = SocketIOChannelProxy(request.environ["socketio"])

        # check that this is actually a websocket request. The session will be
        # `None` if not
        if socket.session:
            # store the request and socket objects in the client dict
            CLIENTS[socket.session.session_id] = (request, socket)

            try:
                while True:
                    # wait for messages
                    message = socket.recv()
                    if len(message):
                        if message[0] == '__subscribe__':
                            # subscribe the socket to the channel
                            socket.subscribe(message[1])
                            events.on_subscribe.send(request, socket, channel=message[1])
                        elif message[0] == '__unsubscribe__':
                            # unsubscribe the socket from channel
                            socket.unsubscribe(message[1])
                            events.on_unsubscribe.send(request, socket, channel=message[1])
                        else:
                            # handle regular messages
                            events.on_message.send(request, socket, message)
                    elif not socket.connected():
                        events.on_disconnect.send(request, socket)
                        break
                return Response('')
            except Exception, e:
                raise e
        raise NotFound()
