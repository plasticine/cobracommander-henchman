import subprocess

class Step(object):
  """
  A Step represents in individual command or task that makes up a build.
  """

  def __init__(self, local_path, command):
    self.local_path = local_path
    self.command = command
    self.stdout = subprocess.PIPE
    self.stderr = subprocess.PIPE
    self.process = None

  def execute(self):
    self.process = subprocess.Popen(self.command, cwd=self.local_path, shell=True,
      stdout=self.stdout, stderr=self.stderr)
