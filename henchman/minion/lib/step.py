

class Step(object):
  """
  A Step represents in individual command or task that makes up a build.
  """

  def __init__(self, cwd, command):
    self.cwd = cwd
    self.command = command
    self.process = None

  def execute(self):
    self.process = subprocess.Popen(self.command, cwd=self.cwd, shell=True,
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
