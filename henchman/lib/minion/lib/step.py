import subprocess

PASSED = lambda x: x == 0
FAILED = lambda x: x != 0 or x > 0

class Step(object):
  """
  A Step represents in individual command or task that makes up a build.
  """

  def __init__(self, local_path, command):
    self.local_path = local_path
    self.command = command
    self._stdout = subprocess.PIPE
    self._stderr = subprocess.PIPE

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
      cwd     = self.local_path,
      shell   = True,
      stdout  = self._stdout,
      stderr  = self._stderr
    )
    self._returncode = self._process.returncode

