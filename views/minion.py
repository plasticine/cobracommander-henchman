from werkzeug.wrappers import Response

def new(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.
    """
    return Response('new')
