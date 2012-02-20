from django.conf import settings
from os import path, chmod
import subprocess
import json

from .step import Step


class SnakeFileNotExecutionError(Exception):
   pass

class SnakeFileValidationError(Exception):
   pass

class SnakeFileJSONError(Exception):
   pass


class Snakefile(object):
   """
   Wrap up loading and parsing/validation of snakefiles.

   The snakefile requires a path param, which will be used when
   self.load() is called to;
   - mark the file as executable
   - execute the file and store the result
   - validate that the output of the snakefile is valid and meets all requirements
   """

   def __init__(self, path):
      self.path = path
      self._stderr = stderr=subprocess.PIPE

   def __getitem__(self, key):
      return self._snakefile[key]

   def __len__(self):
      return len(self._snakefile)

   def load(self):
      self._set_permissions()
      self._execute()
      self._load_json()
      self._validate()
      # self._wrap_build_steps()

   def _set_permissions(self):
      chmod(self.path, 0777)

   def _execute(self):
      try:
         self._snakefile_output = subprocess.check_output(
            self.path,
            shell=True,
            stderr=self._stderr
         )
      except Exception, e:
         raise SnakeFileNotExecutionError(e)

   def _load_json(self):
      try:
         self._snakefile = json.loads(self._snakefile_output)
      except Exception, e:
         raise SnakeFileJSONError(e)

   def _validate(self):
      try:
         assert 'build' in self._snakefile, "Your Snakefile is missing a 'build' attribute."
         assert len(self._snakefile['build']) > 0, "You have not defined any build steps in your snakefile."
      except AssertionError, e:
         raise SnakeFileValidationError(e)

   def _wrap_build_steps(self):
      self._snakefile['build'] = map(lambda x: Step(command=x), self._snakefile['build'])
