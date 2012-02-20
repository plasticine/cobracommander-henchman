import gevent
import os
from django_socketio import events
from django.conf import settings
from django.utils import simplejson as json

from cobracommander.apps.build.models import Build

from .git import Git
from .snakefile import Snakefile

from ..utils.json_encoder import ModelJSONEncoder
from ..utils.socketio import broadcast_channel
from ..utils.logger import get_logger

WAITING     = 0 # waiting to be executed
ACTIVE      = 1 # currently executing
STOPPED     = 2 # stopped for some reason, paused?
COMPLETE    = 3 # complete, we dont care if it passed or failed as long as it is done

class Minion(object):
    """
    Each Minion is a worker process that represents a build.
    """

    def __init__(self, id):
        self.build = self._get_build(id)
        self.cwd = os.path.join(settings.BUILD_ROOT, self.build.uuid)
        self._log = list()
        self._status = WAITING
        self._steps = []
        self._logger = get_logger(__name__)

    def __repr__(self):
        return "<%s build_id='%s' build_uuid='%s' status='%s'>" % ("Minion", self.build.id, self.build.uuid, self.status)

    @property
    def is_waiting(self):
        return self._status == WAITING

    @property
    def is_complete(self):
        return self._status == COMPLETE

    @property
    def status(self):
        return('waiting', 'active', 'stopped', 'complete',)[self._status]

    @property
    def passed(self):
        if self.is_complete:
            return not False in [x.passed for x in self._steps]
        return None

    def start(self):
        """
        Starts the build process, which goes something like this;
        x Set up websocket
        - Clone the git repo to local filesystem
        - Read Snakefile
        - Start Running build
        - Finish running build
        - Clean up git repo?
        - Save necessary things to DB.
        """
        self._status = ACTIVE
        self.greenlet = gevent.Greenlet(self._run)
        self.greenlet.start()

    def stop(self):
        self.greenlet.kill()
        self._status = COMPLETE

    def _save(self):
        for step in self._steps:
            print step

    def _get_build(self, id):
        return Build.objects.select_related().get(id=id)

    def _run(self):
        try:
            self._update_repo()
            self._read_snakefile()
            self._execute_steps()
            self._save()
            self._cleanup()
        except Exception, e:
            self._cleanup()
            raise e

    def _update_repo(self):
        self._logger.info('updating repo')
        Git(cwd = self.cwd, refspec = self.build.target.refspec,
            remote_url = self.build.project.url)

    def _read_snakefile(self):
        self._logger.info('read snakefile')
        self.snakefile = Snakefile(self.cwd).load()

    def _execute_steps(self):
        self._logger.info('execute build steps')
        for step in self.snakefile['build']:
            step.execute()
            self._steps.append(step)

    def _cleanup(self):
        self._logger.info('perform port-execution clean up')
        self._status = COMPLETE
        self.greenlet.join()


