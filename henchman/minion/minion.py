

class Minion(object):
    """
    Each Minion is a worker process that represents a build.
    """

    def __init__(self, build_id):
        self.build_id = build_id

    def start(self):
        pass

    def stop(self):
        pass

    def cleanup(self):
        pass
