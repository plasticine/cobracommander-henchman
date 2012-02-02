from werkzeug.routing import Map, Rule
from .views import static, socketio, builds

urls = Map([
    Rule('/', endpoint=static.root),
    Rule('/builds/new', methods=['post'], endpoint=builds.new),
    Rule('/socket.io/<method>', endpoint=socketio.SocketIOHandler())
])
