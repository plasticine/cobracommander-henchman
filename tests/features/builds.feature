Feature: Managing Builds
  In order for builds to be managed we need to provide an interface
  As Programmer
  I want to be able to manage Builds via POST requests to Henchman

  Scenario: Queue a new Build
    Given we need to run a new build
    When Henchman recieves a POST request to create a build
    Then Henchman creates a new build and appends it to the build-queue

  Scenario: Stop a Build
    Given a Build is currently being run by Henchamn
    When Henchman recieves a POST request to stop the build
    Then Henchman will stop the build and kill the Minion

  Scenario: Cancel a scheduled Build
    Given a Build is scheduled in the build queue
    When Henchman recieves a POST request to stop the build
    Then Henchman will remove the Build from the queue

