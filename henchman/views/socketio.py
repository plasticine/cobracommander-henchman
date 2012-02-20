import sys

from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound

from django_socketio import events
from django_socketio.channels import SocketIOChannelProxy
from django_socketio.clients import client_start, client_end
from django_socketio.clients import CLIENTS

class SocketIOHandler(object):

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

        client_start(request, socket, context)
        try:
            if socket.on_connect():
                events.on_connect.send(request, socket, context)

            while True:
                message = socket.recv()
                if not messages and not socket.connected():
                    events.on_disconnect.send(request, socket, context)
                    break
                # Subscribe and unsubscribe messages are in two parts, the
                # name of either and the channel, so we use an iterator that
                # lets us jump a step in iteration to grab the channel name
                # for these.
                messages = iter(messages)
                for message in messages:
                    if message == "__subscribe__":
                        message = messages.next()
                        message_type = "subscribe"
                        socket.subscribe(message)
                        events.on_subscribe.send(request, socket, context, message)
                    elif message == "__unsubscribe__":
                        message = messages.next()
                        message_type = "unsubscribe"
                        socket.unsubscribe(message)
                        events.on_unsubscribe.send(request, socket, context, message)
                    else:
                        # Socket.IO sends arrays as individual messages, so
                        # they're put into an object in socketio_scripts.html
                        # and given the __array__ key so that they can be
                        # handled consistently in the on_message event.
                        message_type = "message"
                        if message == "__array__":
                            message = messages.next()
                        events.on_message.send(request, socket, context, message)
        except Exception, exception:
            events.on_error.send(request, socket, context, exception)
            raise exception

        events.on_finish.send(request, socket, context)
        client_end(request, socket, context)
        return Response("")
