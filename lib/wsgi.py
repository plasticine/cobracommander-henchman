import os

from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from jinja2 import Environment, FileSystemLoader

class WSGIWebsocketBase(object):
    """
    Setup up basic functions afor WSGI app; dispatch of request response,
    etc...
    """
    def __init__(self):
        self.template_path = os.path.join(os.path.dirname(__file__), '../templates')
        self.jinja = Environment(loader=FileSystemLoader(self.template_path),
                            autoescape=True)

    def application(self, environ, start_response):
        """
        Set up the response cycle
        """
        try:
            response = self.dispatch(Request(environ))
            return response(environ, start_response)
        except HTTPException, e:
            return e(environ, start_response)

    def dispatch(self, request):
        """
        dispatch the matched request to the view function based on on_*viewname*
        pattern. Will pass websocket object to view if it is present in the
        request environment
        """
        urls = self.urls.bind_to_environ(request.environ)
        endpoint, args = urls.match()
        return endpoint(self, request, **args)

    def render(self, template_name, **context):
        template = self.jinja.get_template(template_name)
        return Response(template.render(context), mimetype='text/html')
