from werkzeug.wrappers import Response

def root(server, request):
    return server.render('index.html')
