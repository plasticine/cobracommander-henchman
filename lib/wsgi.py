from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound

from collections import defaultdict

class WSGIWebsocketBase(object):
    """
    Setup up basic functions afor WSGI app; dispatch of request response,
    etc...
    """

    def application(self, environ, start_response):
        """
        Set up the response cycle
        """
        response = self.dispatch(Request(environ))
        return response(environ, start_response)

    def dispatch(self, request):
        """
        dispatch the matched request to the view function based on on_*viewname*
        pattern. Will pass websocket object to view if it is present in the
        request environment
        """
        adapter = self.urls.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        return endpoint(request, **values)
