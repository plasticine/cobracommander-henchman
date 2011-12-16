from git import *
from django.conf import settings

class Git(object):
  """
  Handle cloning a project remote repo.

  Creates a local cache of the remote for the first run and then use this to
  create additional copies for each of the project build targets on first run
  of each of them.

  This allows for quicker creation of new build-targets for the project (we
  can just update & copy then just cached repo and then `reset --hard` onto
  the required target within the copy, saving us from a full git clone each
  time.) It also means that we can properly sandbox the codebase for each
  build-target from the others — allowing for the possibility of having two
  build-targets for the same project executing in parallel.
  """

  def __init__(self, url, uuid):
    self.url = url
    self.uuid = uuid
    self.path = os.path.join(settings.BUILD_ROOT, self.uuid)

  def clone(self):
    pass

  def rebase(self):
    git = repo.git
    git.reset('head', hard=True)

  def update(self, refspec):
    pass
