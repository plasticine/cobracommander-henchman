import subprocess

PASSED = lambda x: x == 0
FAILED = lambda x: x != 0 or x > 0

class Step(object):
  """
  A Step represents in individual command or task that makes up a build.
  """

  def __init__(self, cwd, command):
    self.cwd = cwd
    self.command = command

  @property
  def passed(self):
    return PASSED(self.returncode())

  @property
  def failed(self):
    return FAILED(self.returncode())

  def returncode(self):
    return self._returncode

  def execute(self):
    self._process = subprocess.Popen(
      self.command,
      cwd     = self.cwd,
      shell   = True,
      stdout  = subprocess.PIPE,
      stdin   = subprocess.PIPE
    )
    self._stdout, self._stderr = self._process.communicate(None)
    self._returncode = self._process.returncode

