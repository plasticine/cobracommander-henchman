from os import path
from git import *

class GitWrapper(object):
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

  def __init__(self, url, repo_path, uuid, refspec):
    self.url = url
    self.repo_path = repo_path
    self.uuid = uuid
    self.refspec = refspec
    self._update()

  def _clone(self):
    Git().clone(self.url, self.repo_path)
    self.repo = Repo(self.repo_path)
    self.repo.git.reset(self.refspec, hard=True)

  def _rebase(self):
    self.repo = Repo(self.repo_path)
    self.repo.git.reset(self.refspec, hard=True)

  def _update(self):
    if path.exists(self.repo_path):
      self._rebase()
    else:
      self._clone()
