Feature: Build the searchable recipe-box index
  As a visitor to the recipe collection
  I want a searchable index of all recipes
  So that I can find meals by name, description, difficulty, or time

  Background:
    Given recipe XML files exist under "recipe-system/recipes/"
    And "recipe-system/scripts/cookbook-pkg.py" is available

  Scenario: Build recipe-box.html from the XML catalog
    When I run "python3 cookbook-pkg.py" from "recipe-system/scripts"
    Then "recipe-system/web/recipe-box.html" is generated
    And the page embeds metadata for each recipe (title, description, tags, difficulty, time)
    And each recipe links to its generated page under "recipes/"

  Scenario: Search recipes by text in the recipe box
    Given "recipe-system/web/recipe-box.html" has been generated
    When a visitor enters a search term in the search input
    And they trigger search
    Then recipes whose title or description match the term remain visible
    And non-matching recipes are hidden from the results list

  Scenario: Filter recipes by difficulty or cook time
    Given "recipe-system/web/recipe-box.html" has been generated
    When a visitor activates a difficulty or time filter tag
    Then only recipes matching the active filters are shown
