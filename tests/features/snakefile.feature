Feature: builds are defined by a file (snakefile) in the project codebase

  @wip
  Scenario: Snakefile is executed and parsed into a Snakefile object
    Given that we have a valid Snakefile
    And the Snakefile is executable
    When the Snakefile is executed
    Then a Snakefile object is returned
    And the Snakefile object contains the parsed file

  Scenario: Snakefile cannot be executed
    Given that we have a valid Snakefile
    And the Snakefile is not executable
    When the Snakefile is executed
    Then a SnakeFileNotExecutable exception is raised

  Scenario: Snakefile is malformed and cannot be parsed as JSON
    Given that we have a malformed Snakefile
    And the Snakefile is executable
    When the Snakefile is executed
    Then a SnakeFileJSONError exception is raised

  Scenario: Snakfile does not contain any build step definitions
    Given that we have an invalid Snakefile
    And the Snakefile is executable
    When the Snakefile is executed
    Then a SnakeFileValidationError exception is raised
