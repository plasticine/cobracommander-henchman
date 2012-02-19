from behave import *
import requests
from mock import Mock
from cobracommander.apps.build.models import Build, Target
from cobracommander.apps.project.models import Project

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
