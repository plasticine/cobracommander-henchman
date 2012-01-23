from behave import *
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

@given(u'a build exists with id "1234"')
def step(context):

    print Project.objects.all()
    print Target.objects.all()
    print Build.objects.all()

    context.build = Build.objects.create(project=context.project, target=context.target)

    print Build.objects.all()
    
    context.target.builds.add(context.build)
    context.target.save()

    # print context.client.get('/')
    assert False

@when(u'a POST request to add a new build is recieved')
def step(context):
    assert False

@when(u'the POST data contains build id value of "1234"')
def step(context):
    assert False

@when(u'the build id is valid')
def step(context):
    assert False

@then(u'the build id is appended to the queue.')
def step(context):
    assert False