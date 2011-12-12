

class Minion(object):
    """
    Each Minion is a worker process that represents a build.
    """

    def __init__(self, id):
        self.build_id = id

    def __repr__(self):
        return "<%s build_id=%s status=%s>" % ("Minion", self.build_id, self.status())

    def status(self):
        """
        Returns the status of the minion
        """
        return "waiting"

    def start(self):
        pass

    def stop(self):
        pass

    def cleanup(self):
        pass
