import subprocess

PASSED = 0
FAILED = not 0

class Step(object):
  """
  A Step represents in individual command or task that makes up a build.
  """

  def __init__(self, local_path, command):
    self.local_path = local_path
    self.command = command
    self._stdout = subprocess.PIPE
    self._stderr = subprocess.PIPE
    self._process = None
    self._returncode = None

  @property
  def passed(self):
    return PASSED == self._returncode

  @property
  def failed(self):
    return FAILED == self._returncode

  def returncode(self):
    return self._returncode

  def execute(self):
    self.process = subprocess.Popen(
      self.command,
      cwd     = self.local_path,
      shell   = True,
      stdout  = self._stdout,
      stderr  = self._stderr
    )
    self._returncode = self._process.returncode

