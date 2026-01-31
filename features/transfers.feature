Feature: Account transfers

  Scenario: Successful incoming transfer
    Given Account registry is empty
    And I create an account using name: "Elon", last name: "Musk", pesel: "55555555555"
    When I make an incoming transfer of "1000" to account with pesel "55555555555"
    Then Account with pesel "55555555555" has "balance" equal to "1000"

  Scenario: Successful outgoing transfer
    Given Account registry is empty
    And I create an account using name: "Jeff", last name: "Bezos", pesel: "66666666666"
    And I make an incoming transfer of "500" to account with pesel "66666666666"
    When I make an outgoing transfer of "200" from account with pesel "66666666666"
    Then Account with pesel "66666666666" has "balance" equal to "300"

  Scenario: Failed outgoing transfer due to insufficient funds
    Given Account registry is empty
    And I create an account using name: "Bill", last name: "Gates", pesel: "77777777777"
    And I make an incoming transfer of "100" to account with pesel "77777777777"
    When I make an outgoing transfer of "200" from account with pesel "77777777777"
    Then The transfer should fail with status code "422"
    And Account with pesel "77777777777" has "balance" equal to "100"