import gevent
import os
from django_socketio import events, broadcast_channel, NoSocket
from django.conf import settings

from cobracommander.apps.build.models import Build

from django.utils import simplejson as json
from henchman.lib.json_encoder import ModelJSONEncoder
from .lib.git_wrapper import GitWrapper
from .lib.snakefile import Snakefile

WAITING     = 0
ACTIVE      = 1
STOPPED     = 2
INACTIVE    = 3

class Minion(object):
  """
  Each Minion is a worker process that represents a build.
  """

  def __init__(self, id):
    self._status = WAITING
    self.build = Build.objects.select_related().get(id=id)
    self.local_path = os.path.join(settings.BUILD_ROOT, self.build.uuid)
    self.channel = "build_%s_console" % self.build.uuid
    self._log = list()
    events.on_subscribe(channel=self.channel, handler=self._on_subscribe)

  def __repr__(self):
    return "<%s build_id='%s' build_uuid='%s' status='%s'>" % ("Minion",
      self.build.id, self.build.uuid, self.status)

  @property
  def is_waiting(self):
    return self._status == WAITING

  @property
  def status(self):
    return('waiting', 'active', 'stopped', 'inactive',)[self._status]

  def start(self):
    """
    Starts the build process, which goes something like this;
    x Set up websocket
    - Clone the git repo to local filesystem
    - Read Snakefile
    - Start Running build
    - Finish running build
    - Clean up git repo?
    - Save necessary things to DB.
    """
    self._status = ACTIVE
    self.greenlet = gevent.Greenlet(self._run)
    self.greenlet.start()

  def _run(self):
    self._broadcast('git')
    self.git_wrapper = GitWrapper(build=self.build, local_path=self.local_path)

    self._broadcast('snakefile')
    self.snakefile = Snakefile(local_path=self.local_path)

    print self.snakefile.snakefile

    self._broadcast('build')
    for step in self.snakefile['build']:
      step.execute()
      while step.process.poll() is None:
        self._broadcast(step.process.stdout.readline())

    self._broadcast('cleanup')
    self.cleanup()

  def stop(self):
    self.greenlet.kill()
    self._status = STOPPED

  def cleanup(self):
    self._status = STOPPED
    self.greenlet.join()

  def _broadcast(self, data):
    data = json.dumps(data, cls=ModelJSONEncoder)
    self._log.append(data)
    try:
      broadcast_channel(data, self.channel)
    except NoSocket, e:
      print e

  def _on_subscribe(self, request, socket, context, message):
    """
    New clients should recieve the buffer of the full console output.
    """
    data = json.dumps(self._log, cls=ModelJSONEncoder)
    socket.send(data)
