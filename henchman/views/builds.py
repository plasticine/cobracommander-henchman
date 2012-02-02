import logging
logger = logging.getLogger(__name__)
from werkzeug.wrappers import Response

def new(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.
    """
    if request.method == 'POST':
        build_id = request.form['id']
        server.buildqueue.append(id=build_id)
        return Response('Build id=%s appended tobuildqueue.' % build_id)
    return Response(status=400)
