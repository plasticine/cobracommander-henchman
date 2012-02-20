from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from henchman.minion.snakefile import Snakefile, \
SnakeFileValidationError, SnakeFileJSONError, SnakeFileExecutionError

@given(u'that we have a valid Snakefile')
def step(context):
    context.snakefile_filename = 'valid_snakefile.py'

@given(u'that we have a malformed Snakefile')
def step(context):
    context.snakefile_filename = 'malformed_snakefile.sh'

@given(u'that we have an invalid Snakefile')
def step(context):
    context.snakefile_filename = 'invalid_snakefile.py'

@when(u'the Snakefile is loaded')
def step(context):
    # Create a new Snakefile object. This is wrapped in a try/except so we
    # can capture the exceptions raised to test them properly.
    MockSnakefile = Mock(wraps=Snakefile)
    context.snakefile = MockSnakefile(
        cwd=context.fixture_path('snakefile'),
        snakefile_filename=context.snakefile_filename
    )
    try:
        context.snakefile.load()
    except Exception, e:
        pass

@then(u'the returned Snakefile object contains the parsed file')
def step(context):
    assert hasattr(context.snakefile, '_snakefile')
    assert 'build' in context.snakefile._snakefile

@given(u'the Snakefile is not executable')
def step(context):
    # Set permissions to something non-executable and mock out the
    # permissions method on the Snakefile object
    from os import chmod, path
    chmod(path.join(context.fixture_path('snakefile'), context.snakefile_filename), 0666)
    Snakefile._set_permissions = Mock()

@then(u'a SnakeFileExecutionError exception is raised')
def step(context):
    assert_raises(SnakeFileExecutionError, context.snakefile.load)

@then(u'a SnakeFileJSONError exception is raised')
def step(context):
    assert_raises(SnakeFileJSONError, context.snakefile.load)

@then(u'a SnakeFileValidationError exception is raised')
def step(context):
    assert_raises(SnakeFileValidationError, context.snakefile.load)
