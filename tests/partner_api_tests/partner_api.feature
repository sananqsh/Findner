Feature: Partner API

  Scenario: Create a partner
    When I create a partner with the following details:
      | id | tradingName     | ownerName | document             | coverageArea | address           |
      | 1  | Test Partner    | John Doe  | 123456789/abcdef.something | MultiPolygon | -46.57421, -21.785741 |
    Then the response status code should be 201
    And the response should contain the following details:
      | field           | value                  |
      | id              | 1                      |
      | tradingName     | Test Partner           |
      | document        | 123456789/abcdef.something |
      | coverageArea    | MultiPolygon           |

  Scenario: Create a partner with duplicate document
    When I create a partner with the following details:
      | id | tradingName     | ownerName | document             | coverageArea | address           |
      | 1  | Test Partner    | John Doe  | 123456789/abcdef.something | MultiPolygon | -46.57421, -21.785741 |
    Then the response status code should be 400
    And the response should contain the following details:
      | field           | value                            |
      | detail          | Document already registered      |

  Scenario: Create a partner with existing id
    When I create a partner with the following details:
      | id | tradingName     | ownerName | document                      | coverageArea | address           |
      | 1  | Test Partner    | John Doe  | 123456789/abcdef.somethingNew | MultiPolygon | -46.57421, -21.785741 |
    Then the response status code should be 400
    And the response should contain the following details:
      | field           | value                   |
      | detail          | Id already exists       |

  Scenario: Create a partner after resolving duplication
    When I create a partner with the following details:
      | id | tradingName     | ownerName | document             | coverageArea | address           |
      | 11 | Test Partner    | John Doe  | 123456789/abcdef.something | MultiPolygon | -46.57421, -21.785741 |
    Then the response status code should be 201

  Scenario: Read partners
    When I read partners
    Then the response status code should be 200
    And the response should be a list

  Scenario: Read nearest covering partner
    When I read the nearest covering partner with longitude "123.456" and latitude "12.345"
    Then the response status code should be 404
    And the response should contain the following details:
      | field           | value               |
      | detail          | Partner not found   |

  Scenario: Read nearest covering partner (success)
    When I read the nearest covering partner with longitude "30" and latitude "30"
    Then the response status code should be 200
    And the response should contain the following details:
      | field           | value               |
      | id              | 1                   |
      | tradingName     | Test Partner        |

  Scenario: Read nearest covering partner after adding another partner
    When I create a partner with the following details:
      | id | tradingName        | ownerName | document                | coverageArea | address           |
      | 2  | Harry Somethinger  | Ab Boss   | 987/abc.something-new   | MultiPolygon | -20.57421, -21.785741 |
    Then the response status code should be 200
    And the response should contain the following details:
      | field           | value                 |
      | id              | 2                     |
      | tradingName     | Harry Somethinger     |
