from behave import *
import requests
from mock import Mock
from nose.tools import eq_, ok_, assert_raises

from cobracommander.apps.build.models import Build, Target
from cobracommander.apps.project.models import Project
from henchman.lib.minion.minion import WAITING, ACTIVE, STOPPED, COMPLETE

@given(u'that a project called "{name}" exists')
def step(context, name):
    context.project = Project.objects.create(name=name)
    context.target = Target.objects.create(project=context.project, refspec='master')
    context.project.targets.add(context.target)
    context.project.save()

@given(u'a build exists with id "{id}"')
def step(context, id):
    context.build = Build.objects.create(**{
        'pk':           id,
        'project':      context.project,
        'target':       context.target
    })
    context.target.builds.add(context.build)
    context.target.save()

@when(u'a POST to add a new build is made with a build id value of "{id}"')
def step(context, id):
    context.henchman.buildqueue.append = Mock()
    context.post_response = context.client.post('/builds/new', data={'id':id})

@when(u'a POST to add a new build is made with no build id')
def step(context):
    context.post_response = context.client.post('/builds/new', data={})

@then(u'the response status is "{status_code}"')
def step(context, status_code):
    assert context.post_response.status_code == int(status_code)

@then(u'the build id "{id}" is appended to the queue.')
def step(context, id):
    context.henchman.buildqueue.append.assert_called_with(id=id)

@when(u'a build with id "{id}" is added to the build queue')
def step(context, id):
    def _wrap_minion(id):
        # we need to monkey patch the run method to prevent it from actually running
        # the build, but we need to it to clean itself up to check that states are set.
        minion = Minion(id=id)
        minion._update_repo = Mock()
        minion._read_snakefile = Mock()
        minion._execute_steps = Mock()
        minion._clean_queue = Mock()
        return minion
    context.henchman.buildqueue._wrap_minion = _wrap_minion

    context.henchman.buildqueue.append(int(id))
    eq_(len(context.henchman.buildqueue), 1)
    assert isinstance

@then(u'the build will be started automatically')
def step(context):
    # we need to sleep here to test that the build willbe automatically picked
    # up. The build queue is monitored in an async process so thus we must wait.
    import time; time.sleep(0.001)
    minion = context.henchman.buildqueue._completed[0]

    # check that all out mocked out methods were called, this way we know that
    # the minion was pulled off the queue and executed
    assert minion._update_repo.called
    assert minion._read_snakefile.called
    assert minion._execute_steps.called
    eq_(minion._status, COMPLETE)

@then(u'the build queue will be empty')
def step(context):
    # Need to wait for the queue to be cleaned up in the async process
    import time; time.sleep(0.001)
    eq_(len(context.henchman.buildqueue), 0)
