from gevent import monkey; monkey.patch_all()
from os import path
import subprocess

from django.conf import settings

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

  def __init__(self, build, local_path):
    self.build = build
    self.local_path = local_path
    self.remote_url = self.build.project.url
    self.refspec = "origin/%s" % self.build.target.refspec
    self._update()

  def _git(self, command):
    command = "`which git` %s" % command
    return subprocess.Popen(command, cwd=settings.BUILD_ROOT, shell=True,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

  def _clone(self):
    """
    git clone repo path
    git reset --hard refspec
    """
    self._git('clone %s %s' % (self.remote_url, self.local_path))
    self._git('reset --hard %s' % (self.refspec))

  def _reset(self):
    """
    git reset --hard refspec
    """
    self._git('reset --hard %s' % (self.refspec))

  def _update(self):
    if path.exists(self.local_path):
      self._reset()
    else:
      self._clone()
    return
