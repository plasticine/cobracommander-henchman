#!/usr/bin/env python
# encoding: utf-8
import json

config = {
  'environment':{
    'DJANGO_SETTINGS_MODULE':'settings.test'
  },
  'build':[
    'behave tests'
  ],
  'hooks':{
    'before_build':['git clean -dfx'],
    'after_passing':['say "Success"'],
    'after_failing':['say "Fail"']
    # 'after_build':[]
  }
}

print json.dumps(config)
