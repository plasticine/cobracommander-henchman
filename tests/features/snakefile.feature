Feature: builds are defined by a file (snakefile) in the project codebase

  Scenario: Snakefile is executed and parsed into a Snakefile object
    Given that we have a valid Snakefile
    When the Snakefile is loaded
    Then the returned Snakefile object contains the parsed file

  Scenario: Snakefile cannot be executed
    Given that we have a valid Snakefile
    And the Snakefile is not executable
    When the Snakefile is loaded
    Then a SnakeFileNotExecutionError exception is raised

  Scenario: Snakefile is malformed and cannot be parsed as JSON
    Given that we have a malformed Snakefile
    When the Snakefile is loaded
    Then a SnakeFileJSONError exception is raised

  Scenario: Snakfile does not contain any build step definitions
    Given that we have an invalid Snakefile
    When the Snakefile is loaded
    Then a SnakeFileValidationError exception is raised
