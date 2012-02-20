from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from henchman.lib.minion.lib.snakefile import Snakefile, \
SnakeFileValidationError, SnakeFileJSONError, SnakeFileNotExecutionError

@given(u'that we have a valid Snakefile')
def step(context):
    context.snakefile_path = context.fixture_path('snakefile/valid_snakefile.py')

@given(u'that we have a malformed Snakefile')
def step(context):
    context.snakefile_path = context.fixture_path('snakefile/malformed_snakefile.sh')

@given(u'that we have an invalid Snakefile')
def step(context):
    context.snakefile_path = context.fixture_path('snakefile/invalid_snakefile.py')

@when(u'the Snakefile is loaded')
def step(context):
    # Create a new Snakefile object. This is wrapped in a try/except so we
    # can capture the exceptions raised to test them properly.
    MockSnakefile = Mock(wraps=Snakefile)
    context.snakefile = MockSnakefile(path=context.snakefile_path)
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
    from os import chmod
    chmod(context.snakefile_path, 0666)
    Snakefile._set_permissions = Mock()

@then(u'a SnakeFileNotExecutionError exception is raised')
def step(context):
    assert_raises(SnakeFileNotExecutionError, context.snakefile.load)

@then(u'a SnakeFileJSONError exception is raised')
def step(context):
    assert_raises(SnakeFileJSONError, context.snakefile.load)

@then(u'a SnakeFileValidationError exception is raised')
def step(context):
    assert_raises(SnakeFileValidationError, context.snakefile.load)
