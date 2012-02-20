class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

@given(u'that we have an empty build queue')
def step(context):
    context.henchman.buildqueue._queue = []
