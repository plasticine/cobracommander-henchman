Feature: new builds can be added to the build queue

  Scenario: recieve a POST request with a valid build id
    Given that we have an empty build queue
      And a build exists with id "1234"
     When a POST request to add a new build is recieved
      And the POST data contains build id value of "1234"
      And the build id is valid
     Then the build id is appended to the queue.

  Scenario: recieve a POST request with a build id that does not exist
    When a POST request to add a new build is recieved
     And a build exists with id "4321"
     And the POST data contains build id value of "1234"
     And the build id is invalid
    Then the response status is "400"

  Scenario: recieve a POST request without a build id
    When a POST request to add a new build is recieved
     And the POST data noes not contains a build id
     Then the response status is "400"

