Feature: Generate individual recipe pages from XML
  As a recipe collection maintainer
  I want valid recipe XML transformed into static HTML pages
  So that each recipe can be viewed in a browser after build

  Background:
    Given recipe XML files exist under "recipe-system/recipes/"
    And the XSLT stylesheet exists at "recipe-system/stylesheets/recipe-style.xsl"
    And "recipe-system/scripts/recipe-gen.py" is available

  Scenario: Transform a valid recipe XML file into HTML
    Given a valid recipe XML file such as "sample-lemon-pasta.xml"
    When I run "python3 recipe-gen.py" from "recipe-system/scripts"
    Then an HTML page is written to "recipe-system/web/recipes/sample-lemon-pasta.html"
    And the HTML reflects the recipe title, ingredients, and preparation steps

  Scenario: Generate pages for every XML recipe in the catalog
    Given one or more "*.xml" files under "recipe-system/recipes/"
    When I run "python3 recipe-gen.py" from "recipe-system/scripts"
    Then each XML basename has a matching "*.html" file under "recipe-system/web/recipes/"
    And missing XML files do not leave orphan generation requirements beyond the current catalog

  Scenario: Apply a page background theme during generation
    Given the generator supports themes "light", "warm", "mint", and "dark"
    When I run "python3 recipe-gen.py --theme warm" from "recipe-system/scripts"
    Then generated recipe HTML pages use the warm theme page background
