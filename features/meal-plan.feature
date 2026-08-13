Feature: Produce a weekly meal plan
  As a household meal planner
  I want a weekly plan biased toward crockpot weekdays and weekend batch/BBQ cooking
  So that weekday dinners stay easy and weekend cooks cover lunch prep

  Background:
    Given "recipe-system/scripts/meal-plan-generator.py" is available

  Scenario: Generate a single-week meal plan
    When I run "python3 meal-plan-generator.py --week 28 --year 2026" from "recipe-system/scripts"
    Then the output includes a titled weekly meal plan for week 28 of 2026
    And each day from Monday through Sunday has a theme and meal suggestion
    And weekday entries favor crockpot or easy meals
    And weekend entries favor large batch or BBQ-style cooking with meal-prep notes

  Scenario: Surface holiday callouts when relevant
    Given the generator includes holiday overrides for known dates
    When I generate a meal plan for a year that includes those holidays
    Then holiday notes are printed for matching dates such as Independence Day BBQ

  Scenario: Stub a full 52-week plan request
    When I run "python3 meal-plan-generator.py --week 52 --year 2026" from "recipe-system/scripts"
    Then the weekly plan for week 52 is produced
    And a 52-week plan generation stub message is printed
