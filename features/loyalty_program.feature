# Feature: Loyalty Program Functionality
# This feature covers the core functionality of managing airline loyalty points.

Feature: Loyalty Program
  As a frequent flyer,
  I want to manage my loyalty points
  So that I can earn and redeem rewards.

  @sanity @critical
  Scenario: Add a new member to the loyalty program
    Given the loyalty program system is initialized
    When I add a new member "John Smith"
    Then the member should be added successfully
    And the member should have 0 points
    And the member should be in the "Bronze" tier

  @sanity
  Scenario: Add points to a member's account
    Given the loyalty program system is initialized
    And there is a member "Jane Doe"
    When I add 5000 points to "Jane Doe"
    Then the points should be added successfully
    And "Jane Doe" should have 5000 points
    And "Jane Doe" should be in the "Silver" tier

  @critical
  Scenario: Redeem points from a member's account
    Given the loyalty program system is initialized
    And there is a member "Robert Johnson" with 10000 points
    When I redeem 3000 points from "Robert Johnson"
    Then the points should be redeemed successfully
    And "Robert Johnson" should have 7000 points
    And "Robert Johnson" should be in the "Silver" tier

  @edgecase
  Scenario: Member tier changes based on points
    Given the loyalty program system is initialized
    And there is a member "Emily Davis"
    When I add 6000 points to "Emily Davis"
    Then "Emily Davis" should be in the "Silver" tier
    When I add 10000 points to "Emily Davis"
    Then "Emily Davis" should be in the "Gold" tier
    When I add 15000 points to "Emily Davis"
    Then "Emily Davis" should be in the "Platinum" tier
    When I redeem 25000 points from "Emily Davis"
    Then "Emily Davis" should be in the "Silver" tier

  @negative
  Scenario: Attempt to redeem more points than available
    Given the loyalty program system is initialized
    And there is a member "Michael Wilson" with 5000 points
    When I attempt to redeem 6000 points from "Michael Wilson"
    Then the redemption should fail
    And "Michael Wilson" should still have 5000 points

  @sanity
  Scenario: Add an existing member
    Given the loyalty program system is initialized
    And there is a member "Sarah Brown"
    When I add a new member "Sarah Brown"
    Then the member should not be added
    
  @negative
  Scenario: Add invalid points
    Given the loyalty program system is initialized
    And there is a member "David Lee"
    When I add -100 points to "David Lee"
    Then the points should not be added
    And "David Lee" should have 0 points
