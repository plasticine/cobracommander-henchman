from henchman.lib.minion.lib.snakefile import Snakefile, \
SnakeFileValidationError, SnakeFileJSONError, SnakeFileNotExecutionError

@given(u'that we have an empty build queue')
def step(context):
    context.henchman.buildqueue._queue = []
