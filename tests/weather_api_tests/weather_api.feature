Feature: Retrieving weather information using OpenWeatherMap API

  Scenario: Retrieve weather information for a valid city
    Given a valid API key for OpenWeatherMap API
    When I send a GET request to retrieve weather information for "London"
    Then the response status code should be 200
    And the response should contain the weather information for "London"

  Scenario: Retrieve weather information for an invalid city
    Given a valid API key for OpenWeatherMap API
    When I send a GET request to retrieve weather information for an invalid city
    Then the response status code should be 404

  Scenario: Retrieve weather information with optional parameters
    Given a valid API key for OpenWeatherMap API
    When I send a GET request to retrieve weather information for "London" with optional parameters
    Then the response status code should be 200
    And the response should contain the weather information based on the specified parameters

  Scenario: Handle rate limiting
    Given a valid API key for OpenWeatherMap API
    When I send multiple GET requests within a short time frame
    Then the response status code should indicate rate limiting exceeded
