from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from henchman.lib.minion.minion import Minion
from henchman.lib.minion.minion import WAITING, ACTIVE, STOPPED, COMPLETE

@when(u'a build with id "{id}" is added to the build queue')
def step(context, id):
    def _wrap_minion(id):
        # we need to monkey patch the run method to prevent it from actually running
        # the build, but we need to it to clean itself up to check that states are set.
        minion = Minion(id=id)
        minion._update_repo = Mock()
        minion._read_snakefile = Mock()
        minion._execute_steps = Mock()
        return minion
    context.henchman.buildqueue._wrap_minion = _wrap_minion

    # short monitor interval so we can speed up testing
    context.henchman.buildqueue._monitor_sleep_time = 0.001

    context.henchman.buildqueue.append(int(id))
    eq_(len(context.henchman.buildqueue), 1)

@then(u'the build will be started automatically')
def step(context):
    # we need to sleep here to test that the build willbe automatically picked
    # up. The build queue is monitored in an async process so thus we must wait.
    import time; time.sleep(0.001)

    # check that all out mocked out methods were called, this way we know that
    # the minion was pulled off the queue and executed
    assert context.henchman.buildqueue._queue[0]._update_repo.called
    assert context.henchman.buildqueue._queue[0]._read_snakefile.called
    assert context.henchman.buildqueue._queue[0]._execute_steps.called
    eq_(context.henchman.buildqueue._queue[0]._status, COMPLETE)

@then(u'the build queue will be empty')
def step(context):
    # Need to wait for the queue to be cleaned up in the async process
    import time; time.sleep(0.001)
    eq_(len(context.henchman.buildqueue), 0)
