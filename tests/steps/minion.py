from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from henchman.minion import Minion, COMPLETE
from henchman.minion.step import Step

@given(u'that we have a build with "{num_steps}" steps')
def step(context, num_steps):
    Minion._update_repo = Mock()
    Minion._get_build = Mock(return_value=Struct(**{
        'id':1, 'uuid':'roflcopter'
    }))
    Minion._read_snakefile = Mock()
    Minion.snakefile = {
        'build':[Mock(name="step_%s" % x) for x in range(int(num_steps))]
    }
    context.minion = Minion(id=999)

@when(u'the minion has completed the build')
def step(context):
    import time; time.sleep(0.01)
    assert context.minion._get_build.called
    assert context.minion._update_repo.called
    assert context.minion._read_snakefile.called
    eq_(context.minion._status, COMPLETE)

@then(u'the minion will have "{num_steps}" step results')
def step(context, num_steps):
    eq_(len(context.minion._steps), int(num_steps))
    for step in context.minion._steps:
        assert step.execute.called
        assert step.passed
