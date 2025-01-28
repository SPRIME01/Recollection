Feature: Capture Screenshot

  Scenario: Successfully capture a screenshot
    Given the system is ready to capture a screenshot
    When I send a request to capture a screenshot
    Then I should receive a success response
    And the response should contain a screenshot with a timestamp, text, embedding, and image path

  Scenario: Retrieve the timeline of screenshots
    Given the system has captured screenshots
    When I send a request to retrieve the timeline
    Then I should receive a list of screenshots
    And each screenshot should have a timestamp, text, embedding, and image path
