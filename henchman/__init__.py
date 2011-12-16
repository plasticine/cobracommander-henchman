__version__ = "0.1"

def setup_environment():
  """
  Set up Henchman to talk to Cobracommander django app by fucking with paths and
  running `django.core.management.setup_environ`
  """
  import sys, os
  sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
  from django.core.management import setup_environ
  from cobracommander import settings as cobracommander_settings
  setup_environ(cobracommander_settings)
