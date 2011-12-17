import gevent
import os

from django.conf import settings

from cobracommander.apps.build.models import Build

from .lib.git_wrapper import GitWrapper
from .lib.snakefile import Snakefile

WAITING = 0
ACTIVE = 1
STOPPED = 1

class Minion(object):
  """
  Each Minion is a worker process that represents a build.
  """

  def __init__(self, id):
    self._status = WAITING
    self._build = Build.objects.select_related().get(id=id)
    self.repo_path = os.path.join(settings.BUILD_ROOT, self._build.uuid)

  def __repr__(self):
    return "<%s build_id='%s' build_uuid='%s' status='%s'>" % ("Minion",
      self._build.id, self._build.uuid, self.status())

  def is_active(self):
    return self._status == ACTIVE

  def status(self):
    return('waiting', 'active',)[self._status]

  def start(self):
    """
    Starts the build process, which goes something like this;
    - Set up websocket
    - Clone the git repo to local filesystem
    - Read Snakefile
    - Start Running build
    - Finish running build
    - Clean up git repo?
    - Save necessary things to DB.
    """
    self._status = ACTIVE
    g = gevent.Greenlet(self._run)
    g.start()
    # self.snakefile = Snakefile(self.repo_path)
    # for step in self.snakefile['build']:
    #   step.execute()
    #   while step.process.poll() is None:
    #     print step.process.stdout.readline()

  def _run(self):
    gitwrapper = GitWrapper(
      self._build.project.url,
      self.repo_path,
      self._build.uuid,
      self._build.target_set.all()[0].refspec
    )

  def stop(self):
    self._status = STOPPED

  def cleanup(self):
    pass
