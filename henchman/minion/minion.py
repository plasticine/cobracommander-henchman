from cobracommander.apps.build.models import Build

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

  def __repr__(self):
    return "<%s build_id='%s' build_uuid='%s' status='%s'>" % ("Minion", self._build.id,
      self._build.uuid, self.status())

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
    self._update_git_repo()

  def stop(self):
    self._status = STOPPED

  def cleanup(self):
    pass

  def _update_git_repo(self):
    repo = Git(url=self._build.project.url, uuid=self._build.uuid)
    repo.update()
