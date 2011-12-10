Feature: Snakefile
  In order to have instructions for running a build be tied to the codebase version
  As a Programmer
  I want to be able to have the instructions for building my project in a Snakefile inside my project codebase

  Scenario: Load a snakefile
    Given I have a snakefile
    When I load the snakefile
    Then the snakefile is parsed
    And a Snakefile instance created from the data

  Scenario: Snakefile is missing required properties
    Given I have a snakefile with missing required properties
    When I load the snakefile
    Then I should check that the required properties have been set
