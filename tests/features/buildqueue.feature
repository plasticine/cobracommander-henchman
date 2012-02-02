@browser
Feature: new builds can be added to the build queue

  Background:
    Given that a project called "foobar" exists

  @wip
  Scenario: recieve a POST request with a valid build id
    Given that we have an empty build queue
      And a build exists with id "1234"
     When a POST to add a new build is made with a build id value of "1234"
     Then the build id is appended to the queue.

  Scenario: recieve a POST request with a build id that does not exist
    When a POST request to add a new build is made
     And the POST data contains build id value of "9999"
    Then the response status is "400"

  Scenario: recieve a POST request without a build id
    When a POST request to add a new build is recieved
     And the POST data noes not contains a build id
     Then the response status is "400"

