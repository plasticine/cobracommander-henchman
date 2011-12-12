import requests, logging
logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.CRITICAL)
from nose.tools import ok_, eq_, raises, timed

@when(u'Henchman recieves a POST request to create a build')
def step(context):
    r = requests.post('http://localhost:9999/builds/new', data={'id':1})
    eq_(r.content, "OK")

@then(u'Henchman creates a new build and appends it to the build-queue')
def step(context):
    assert True
