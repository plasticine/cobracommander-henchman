from .server import HenchmanServer
from .buildqueue import BuildQueue
from .utils.logger import get_logger

class Henchman(HenchmanServer):
    """

    """
    def __init__(self):
        self.logger = get_logger(__name__)
        self.buildqueue = BuildQueue()
        super(Henchman, self).__init__()
