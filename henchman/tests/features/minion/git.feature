Feature: Cloning remote projects via Git
  In order for builds to be built we need to clone the remote repo
  As a Programmer
  I want to be able to have my project code cloned quickly and efficiently so I can start testing faster

  Scenario: New project
    Given a project called "WidgetsApp" does not exist
    When I create a new project called "WidgetsApp"
    And build the default build-target
    Then there should be a cached version of the codebase in the Vault
    And there should be a copy of the codebase for the default build-target in the Vault
