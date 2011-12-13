from ..minion import Minion

class BuildQueue(object):
  """
  The BuildQueue class is used to manage
  """

  def __init__(self):
    self._queue = []
    self.current_item = 0

  def __len__(self):
    return len(self._queue)

  def __iter__(self):
    return self

  def next(self):
    if (self.current_item == len(self._queue)):
        self.current_item = 0
        raise StopIteration
    else:
        data = self._queue[self.current_item]
        self.current_item += 1
        return data

  def append(self, id):
    """
    Create a new Minion instance for `id` and append it to the internal queue list.
    """
    self._queue.append(Minion(id=id))
