import gevent
from ..minion import Minion

class BuildQueue(object):
  """
  The BuildQueue class is used to manage Minions either currently being built
  or waiting to be built.
  """

  def __init__(self):
    self._queue = []
    self.current_item = 0
    gevent.spawn(self.monitor_queue)

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

  def monitor_queue(self):
    """
    Poll `_queue` to see if we need to start a new Minion.
    """
    while True:
      if len(self._queue) and len(filter(lambda x: x.is_active(), self._queue)) < 1:
        self._queue[0].start()
      gevent.sleep(0.5)
