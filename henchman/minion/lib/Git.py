

class Git(object):
    """
    Handle cloning a project remote repo.

    Creates a local cache of the remote for the first run and then use this to
    create additional copies for each of the project build targets on first run
    of each of them.

    This allows for quicker creation of new build-targets for the project (we
    can just update & copy then just cached repo and then `reset --hard` onto
    the required target within the copy, saving us from a full git clone each
    time.) It also means that we can properly sandbox the codebase for each
    build-target from the others — allowing for the possibility of having two
    build-targets for the same project executing in parallel.
    """

    def __init__(self):
        pass
