import gevent
import json

from .minion import Minion
from .utils.logger import get_logger

class BuildQueue(object):
  """
  The BuildQueue class is used to manage Minions either currently being built
  or waiting to be built.

  Defines socket.io methods for subscribing and updating the build queue. These
  are wrapped up on django-socketio events.
  """

  def __init__(self):
    self._queue = []
    self._completed = []
    self._monitor_sleep_time = 1
    self._monitor_hibernate_time = 5
    self._current_item = 0
    self._logger = get_logger(__name__)
    self._logger.info('Monitoring queue for incoming builds')
    gevent.spawn(self._monitor)

  def __len__(self):
    return len(self._queue)

  def __iter__(self):
    return self

  def __getitem__(self, key):
      return self._queue[key]

  def next(self):
    if (self._current_item == len(self._queue)):
      self._current_item = 0
      raise StopIteration
    else:
      data = self._queue[self._current_item]
      self._current_item += 1
      return data

  def append(self, id):
    """
    Create a new Minion instance for `id` and append it to the internal
    queue list.
    """
    self._queue.append(self._wrap_minion(id))
    self._logger.info('Appended new build to queue with id:%s, queue length is now %s', id, len(self._queue))

  def _wrap_minion(self, id):
    return Minion(id=id)

  def _monitor(self):
    """
    Poll `_queue` to see if we need to start a new Minion.
    """
    while True:
      # filter queue for only items that are waiting to execute.
      if len(self._queue):
        if len(filter(lambda x: not x.is_waiting, self._queue)) < 1:
          minion = self._queue[0]
          self._logger.info('Putting minion to work')
          minion.start()
        self._clean_queue()
        self._hibernate()
      gevent.sleep(self._monitor_sleep_time)

  def _hibernate(self):
    self._logger.info('Hibernating for %s seconds', self._monitor_hibernate_time)
    gevent.sleep(self._monitor_hibernate_time)

  def _clean_queue(self):
    """
    remove completed Minions from the build queue and prepend them to the
    complete queue for reference.
    """
    self._logger.info('Cleaning internal build queue')
    completed = self._completed
    complete = [i for i, x in enumerate(self._queue) if x.is_complete]
    [completed.insert(0, self._queue[x]) for x in complete]
    self._completed = completed[:5]
    self._queue[:] = [x for x in self._queue if not x.is_complete]
