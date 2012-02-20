from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from henchman.lib.minion.lib.step import Step
from henchman.lib.minion.minion import COMPLETE, ACTIVE

def mock_steps(context, returncode_value):
    Step.returncode = Mock(return_value=returncode_value)
    Step._process = Mock()
    Step.execute = Mock()

    num_steps = len(context.minion._read_snakefile.return_value['build'])
    steps = [Step('','') for x in range(num_steps)]
    context.minion._read_snakefile = Mock(return_value={'build':steps})

@given(u'all the of the steps have zero return codes')
def step(context):
    mock_steps(context, returncode_value=0)

@given(u'one the of the steps has a non-zero return codes')
def step(context):
    mock_steps(context, returncode_value=1)

@when(u'we start the build')
def step(context):
    context.minion.start()
    eq_(context.minion._status, ACTIVE)

@then(u'the minion has a passing state')
def step(context):
    eq_(context.minion._status, COMPLETE)
    assert context.minion.passed

@then(u'the minion has a failing state')
def step(context):
    eq_(context.minion._status, COMPLETE)
    eq_(context.minion.passed, False)
