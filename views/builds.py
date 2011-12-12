import logging
logger = logging.getLogger(__name__)
from werkzeug.wrappers import Response

def new(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.
    """
    if request.method == 'POST':
        build_id = request.form['id']
        logger.info('New build with id:%s added to BuildQueue', build_id)
        server.queue.append(id=build_id)
        return Response('OK')
