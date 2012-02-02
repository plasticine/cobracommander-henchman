from werkzeug.wrappers import Response
from django_socketio.channels import CHANNELS
from django_socketio.views import CLIENTS

def root(server, request):
    return server.render('index.html', **{
      'queue':    server.buildqueue,
      'clents':   CLIENTS,
      'channels': CHANNELS
    })
