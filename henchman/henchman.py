from .lib import henchman_server, buildqueue

class Henchman(henchman_server.HenchmanServer):
    """docstring for Henchman"""
    def __init__(self):
        self.buildqueue = buildqueue.BuildQueue()
        super(Henchman, self).__init__()




