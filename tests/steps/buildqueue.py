from behave import *
import requests
from cobracommander.apps.build.models import Build, Target
from cobracommander.apps.project.models import Project

@given(u'that a project called "{name}" exists')
def step(context, name):
    context.project = Project.objects.create(name=name)
    context.target = Target.objects.create(project=context.project, refspec='master')
    context.project.targets.add(context.target)
    context.project.save()

@given(u'that we have an empty build queue')
def step(context):
    pass

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
    data = {'id':id}
    context.post_response = context.client.post('/builds/new', data=data)

@then(u'the build id is appended to the queue.')
def step(context):
    assert context.post_response.status_code == 200
    context.client.get('/')
    assert False
