from django_socketio.utils import NoSocket

def send(session_id, message):
    from django_socketio.utils import send
    try:
        send(session_id, message)
    except NoSocket, exception:
        # raise exception
        pass

def broadcast(message):
    from django_socketio.utils import broadcast
    try:
        broadcast(message)
    except NoSocket, exception:
        # raise exception
        pass

def broadcast_channel(message, channel):
    from django_socketio.utils import broadcast_channel
    try:
        broadcast_channel(message, channel)
    except NoSocket, exception:
        # raise exception
        pass
