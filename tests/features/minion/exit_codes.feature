@wip
Feature: build status is determined from the exit-codes of build steps

  Scenario: all build steps return zero exit codes
    Given that we have a build with "2" steps
    And all the of the steps have zero return codes
    When we start the build
    And the minion has completed the build
    Then the minion has a passing state

  Scenario: one build step returns a non-zero exit code
    Given that we have a build with "3" steps
    And one the of the steps has a non-zero return codes
    When we start the build
    And the minion has completed the build
    Then the minion has a failing state
