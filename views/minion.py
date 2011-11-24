from werkzeug.wrappers import Response

def spawn(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.
    """
    return Response('spawn')
