from os import path, chmod
import subprocess
import json

from django.conf import settings

from .step import Step

class InvalidSnakefile(Exception):
   pass


class Snakefile(object):
   """
   Handle the reading and parsing of snakefiles from within Project codebase.

   A Snakefile is a JSON parseable file that tells Cobracommander how to setup
   and build your project.

   The Snakefile is defined by several sections:
   - environment: {} (environment var key/value pairs to be set for the project before the build is started)
   - build: [] (an array of Step objects to be run in sequence in order to execute the build)
   - hooks: [] arrays of hooks to be run at various points before, during and after a build run
      - before_build: []
      - after_passing: []
      - after_failing: []
   """

   def __init__(self, local_path):
      self.snakefile = None
      self.local_path = local_path
      self.snakefile_path = path.join(self.local_path, 'snakefile')

   def __getitem__(self, key):
      self.read()
      return self.snakefile[key]

   def __len__(self):
      self.read()
      return len(self.snakefile)

   def read(self):
      if self.snakefile == None:
         self._contents = self._run_and_return_output()
         self._parse()
      return True

   def _run_and_return_output(self):
      chmod(self.snakefile_path, 0777)
      p = subprocess.Popen(self.snakefile_path, shell=True,
               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      snakefile, err = p.communicate()
      if err == '':
         return snakefile
      raise InvalidSnakefile("Invalid Snakefile: %s", err)

   def _parse(self):
      self.snakefile = json.loads(self._contents)
      try:
         assert 'build' in self.snakefile, "Your Snakefile is missing a 'build' attribute."
         assert len(self.snakefile['build']) > 0, "You have not defined any build steps in your snakefile."
      except AssertionError, e:
         raise InvalidSnakefile("Invalid Snakefile: %s", e)
      self.snakefile['build'] = map(lambda command: Step(local_path=self.local_path, command=command),
                           self.snakefile['build'])
