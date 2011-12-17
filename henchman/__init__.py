__version__ = "0.1"

def setup_environment():
  """
  Set up Henchman to talk to Cobracommander django app by fucking with paths and
  running `django.core.management.setup_environ`
  """
  import sys, os
  from django.core.management import setup_environ

  if 'DJANGO_SETTINGS_MODULE' in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
    name = 'cobracommander.%s' % os.environ['DJANGO_SETTINGS_MODULE']
    __import__(name)
    setup_environ(sys.modules[name])
  else:
    raise
