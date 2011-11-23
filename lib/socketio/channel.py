class SocketIOChannelProxy(object):
    """"""

    def __init__(self, socket):
        """
        Store the original socket protocol object.
        """
        self.socket = socket
        self.channels = []

    def subscribe(self, channel):
        """
        Add the channel to this socket's channels, and to the list of
        subscribed session IDs for the channel. Return False if
        already subscribed, otherwise True.
        """
        if channel in self.channels:
            return False
        CHANNELS[channel].append(self.socket.session.session_id)
        self.channels.append(channel)
        return True

    def unsubscribe(self, channel):
        """
        Remove the channel from this socket's channels, and from the
        list of subscribed session IDs for the channel. Return False
        if not subscribed, otherwise True.
        """
        try:
            CHANNELS[channel].remove(self.socket.session.session_id)
            self.channels.remove(channel)
        except ValueError:
            return False
        return True

    def broadcast(self, channel, message):
        """
        Send the given message to all subscribers for the channel
        given. If no channel is given, send to the subscribers for
        all the channels that this socket is subscribed to.
        """
        for subscriber in CHANNELS[channel]:
            if subscriber != self.socket.session.session_id:
                self._write(message, self.socket.handler.server.sessions[subscriber])

    def __getattr__(self, name):
        """
        Proxy missing attributes to the socket.
        """
        return getattr(self.socket, name)
