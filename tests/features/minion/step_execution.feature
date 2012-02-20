@wip
@db
Feature: a build can have multiple steps that are executed serially

  Scenario: a build is run with one step
    Given that we have an empty build queue
    And that we have a build with "1" steps
    When we start the build
    And the minion has completed the build
    Then the minion will have "1" step results

  Scenario: a build is run with five steps
    Given that we have an empty build queue
    And that we have a build with "5" steps
    When we start the build
    And the minion has completed the build
    Then the minion will have "5" step results
