import gevent
import os
from django_socketio import events, NoSocket
from django.conf import settings

from cobracommander.apps.build.models import Build

from django.utils import simplejson as json
from henchman.lib.json_encoder import ModelJSONEncoder
from henchman.lib.socketio_utils import broadcast_channel
from .lib.git_wrapper import GitWrapper
from .lib.snakefile import Snakefile

WAITING     = 0 # waiting to be executed
ACTIVE      = 1 # currently executing
STOPPED     = 2 # stopped for some reason, paused?
COMPLETE    = 3 # complete, we dont care if it passed or failed as long as it is done

class Minion(object):
  """
  Each Minion is a worker process that represents a build.
  """

  def __init__(self, id):
    self.build = self._get_build(id)
    self.local_path = os.path.join(settings.BUILD_ROOT, self.build.uuid)
    self.channel = "build_%s_console" % self.build.uuid
    self._log = list()
    self._status = WAITING
    self._steps = []
    events.on_subscribe(channel=self.channel, handler=self._on_subscribe)

  def __repr__(self):
    return "<%s build_id='%s' build_uuid='%s' status='%s'>" % ("Minion",
      self.build.id, self.build.uuid, self.status)

  @property
  def is_waiting(self):
    return self._status == WAITING

  @property
  def is_complete(self):
    return self._status == COMPLETE

  @property
  def status(self):
    return('waiting', 'active', 'stopped', 'complete',)[self._status]

  @property
  def passed(self):
    if self.is_complete:
      return not False in [x.passed for x in self._steps]
    return None

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
    self._steps = []
    self.greenlet = gevent.Greenlet(self._run)
    self.greenlet.start()

  def _get_build(self, id):
    return Build.objects.select_related().get(id=id)

  def _run(self):
    self._broadcast('git')
    self._update_repo()

    self._broadcast('snakefile')
    self.snakefile = self._read_snakefile()

    self._broadcast('build')
    self._execute_steps()

    self._broadcast('cleanup')
    self._cleanup()

  def _update_repo(self):
    GitWrapper(build=self.build, local_path=self.local_path)

  def _read_snakefile(self):
    return Snakefile(local_path=self.local_path)

  def _execute_steps(self):
    for step in self.snakefile['build']:
      step.execute()
      while step._process.poll() is None:
        self._broadcast(step._process._stdout.readline())
      self._steps.append(step)

  def _cleanup(self):
    self._status = COMPLETE
    self.greenlet.join()

  def stop(self):
    self.greenlet.kill()
    self._status = COMPLETE

  def _broadcast(self, data):
    data = json.dumps(data, cls=ModelJSONEncoder)
    self._log.append(data)

  def _on_subscribe(self, request, socket, context, message):
    """
    New clients should recieve the buffer of the full console output.
    """
    data = json.dumps(self._log, cls=ModelJSONEncoder)
    socket.send(data)
