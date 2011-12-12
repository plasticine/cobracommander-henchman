from ..minion import Minion

class BuildQueue(object):
  """
  The BuildQueue class is used to manage
  """

  def __init__(self):
    self._queue = []

  def __len__(self):
    return len(self._queue)

  def append(self, id):
    """
    Create a new Minion instance for `id` and append it to the internal queue list.
    """
    self._queue.append(Minion(build_id=build_id))
