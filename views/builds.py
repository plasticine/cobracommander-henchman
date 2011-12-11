from werkzeug.wrappers import Response

def new(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.
    """
    if request.method == 'POST':
        build_id = request.form['id']
        return Response('New build with id:%s added to queue.' % (build_id))
