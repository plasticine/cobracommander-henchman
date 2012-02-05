import gevent
import json
from django_socketio import events, broadcast_channel
from django.utils import simplejson as json
from .json_encoder import ModelJSONEncoder

from .minion import Minion

class BuildQueue(object):
  """
  The BuildQueue class is used to manage Minions either currently being built
  or waiting to be built.

  Defines socket.io methods for subscribing and updating the build queue. These
  are wrapped up on django-socketio events.
  """

  def __init__(self):
    self._queue = []
    self.current_item = 0
    gevent.spawn(self._monitor)
    events.on_subscribe(channel='build_queue', handler=self._on_subscribe)

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
    minion = Minion(id=id)
    self._queue.append(minion)
    data = json.dumps(self._queue, cls=ModelJSONEncoder)
    broadcast_channel(data, 'build_queue')

  def _monitor(self):
    """
    Poll `_queue` to see if we need to start a new Minion.
    """
    while True:
      # filter queue for only items that are waiting to execute.
      if len(self._queue) and len(filter(lambda x: not x.is_waiting, self._queue)) < 1:
        self._queue[0].start()
      gevent.sleep(0.5)

  def _on_subscribe(self, request, socket, context, message):
    """
    New clients should recieve the buffer of all full queue.
    """
    data = json.dumps(self._queue, cls=ModelJSONEncoder)
    socket.send(data)
