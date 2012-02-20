@db
Feature: a build can have multiple steps that are executed serially

  Scenario: a build is run with one step
    Given that we have an empty build queue
    And a build with "1" step is added to the queue
    When the minion has completed the build
    Then the minion will have "1" step results

  Scenario: a build is run with five steps
    Given that we have an empty build queue
    And a build with "5" step is added to the queue
    When the minion has completed the build
    Then the minion will have "5" step results
