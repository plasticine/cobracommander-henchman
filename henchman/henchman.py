from .lib import henchman_server, buildqueue, logger

class Henchman(henchman_server.HenchmanServer):
    """docstring for Henchman"""
    def __init__(self):
        self.logger = logger.get_logger(__name__)
        self.buildqueue = buildqueue.BuildQueue()
        super(Henchman, self).__init__()




