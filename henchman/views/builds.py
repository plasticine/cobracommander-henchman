from werkzeug.wrappers import Response
from cobracommander.apps.build.models import Build

def new(server, request):
    """
    Accepts POST requests containing the id of the build to spawn a minion for.

    If build id is not passed in the POST request, or the build id is invalid
    (the record does not exist) then return a 400.

    If the build id is valid then append the build to the build queue for
    processing.
    """
    if request.method == 'POST':
        build_id = request.form['id']
        try:
            Build.objects.get(id=build_id)
            server.buildqueue.append(id=build_id)
            return Response('Build id=%s appended to buildqueue.' % build_id)
        except Exception, e:
            pass
    return Response(status=400)
