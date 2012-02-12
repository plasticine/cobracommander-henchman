import os

@given(u'that we have a valid Snakefile')
def step(context):
    context.snakefile = os.path.join(context._fixtures_dir,
                            'snakefile/valid_snakefile')

@given(u'the Snakefile is executable')
def step(context):
    print context.snakefile
