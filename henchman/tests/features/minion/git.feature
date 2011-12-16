Feature: Cloning remote projects via Git
  In order for builds to be built we need to clone the remote repo
  As a Programmer
  I want to be able to have my project code cloned quickly and efficiently so I can start testing faster

  Scenario: Clone
    Given I have a uuid for a Project Target of "de76c3e" which does not exist in the Vault
    When I tell Git to update to "master"
    Then I should see the repo checked out in a directory called "de76c3e"
    And the current HEAD should be "master"

  Scenario: Reset Hard
    Given I have a uuid for a Project Target of "f2c844a" which does exist in the Vault
    When I tell Git to update to "foobar"
    Then I should see the repo checked out in a directory called "f2c844a"
    And the current HEAD should be "foobar"

