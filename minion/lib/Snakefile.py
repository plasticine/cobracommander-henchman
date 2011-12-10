

class Snakefile(object):
   """
   Handle the reading and parsing of snakefiles from within Project codebase.

   A Snakefile is a JSON parseable file that tells Cobracommander how to setup
   and build your project.

   The Snakefile is defined by several sections:
   - environment: {} (environment var key/value pairs to be set for the project before the build is started)
   - build: [] (an array of steps to be run in sequence in order to execute the build)
   - hooks: [] arrays of hooks to be run at various points before, during and after a build run
      - before_build: []
      - after_passing: []
      - after_failing: []
   """

   def __init__(self, snakefile):
      pass

   def _parse(self):
      pass
