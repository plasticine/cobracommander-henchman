@wip
@db
Feature: a build is started when there are no builds in progress

  Background:
    Given that a project called "foobar" exists

  Scenario: builds are started automatically when the build queue is empty
    Given that we have an empty build queue
    And a build exists with id "1234"
    When a build with id "1234" is added to the build queue
    Then the build will be started automatically
    And the build queue will be empty


# Feature: a build can have multiple steps that are executed serially

#   Scenario: a build is run with one step
#     Given that we have an empty build queue
#     And a build with "1" step is added to the queue
#     When the minion has completed the build
#     Then the minion will have "1" step results

#   Scenario: a build is run with five steps
#     Given that we have an empty build queue
#     And a build with "5" step is added to the queue
#     When the minion has completed the build
#     Then the minion will have "5" step results


# Feature: build status is determined from the exit-codes of build steps

#   Scenario: all build steps return zero exit codes

#   Scenario: one build step returns a non-zero exit code






# Feature: build hooks can be executed during a build
