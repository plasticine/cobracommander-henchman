@given(u'I have a uuid for a Project Target of "{uuid}" which does not exist in the Vault')
def step(context, uuid):
  assert True

@given(u'I have a uuid for a Project Target of "{uuid}" which does exist in the Vault')
def step(context, uuid):
  assert True

@when(u'I tell Git to update to "{ref}"')
def step(context, ref):
  assert True

@then(u'I should see the repo checked out in a directory called "{uuid}"')
def step(context, uuid):
  assert True

@then(u'the current HEAD should be "{ref}"')
def step(context, ref):
  assert True
