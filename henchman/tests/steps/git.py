from henchman.minion.lib import Git

@given(u'I have a uuid for a Project Target of "{uuid}" which does not exist in the Vault')
def step(context, uuid):
  assert False

@given(u'I have a uuid for a Project Target of "{uuid}" which does exist in the Vault')
def step(context, uuid):
  assert False

@when(u'I tell Git to update to "{ref}"')
def step(context, ref):
  assert False

@then(u'I should see the repo checked out in a directory called "{uuid}"')
def step(context, uuid):
  assert False

@then(u'the current HEAD should be "{ref}"')
def step(context, ref):
  assert False
