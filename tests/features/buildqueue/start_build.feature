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
