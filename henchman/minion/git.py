from gevent import monkey; monkey.patch_all()
from os import path
import subprocess
from pbs import git

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
  build-target from the others.
  """

  def __init__(self, cwd, refspec, remote_url):
    self.cwd = cwd
    self.remote_url = remote_url
    self.refspec = "origin/%s" % refspec

  def update(self):
    if path.exists(self.cwd):
      self._reset()
    else:
      self._clone()
      self._reset()
    return

  def _clone(self):
    """
    git clone repo path
    git reset --hard refspec
    """
    git.clone(self.remote_url, self.cwd)

  def _reset(self):
    """
    git reset --hard refspec
    """
    git.reset(self.refspec, hard=True)
