{
  'environment':{
    'DJANGO_SETTINGS_MODULE':'settings.test'
  },
  'build':[
    'behave ./henchman/tests'
  ],
  'hooks':{
    'before_build':['git clean -dfx'],
    'after_passing':['say "Success"'],
    'after_failing':['say "Fail"']
  }
}
