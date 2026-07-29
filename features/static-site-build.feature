Feature: Build static site output for Vercel
  As a deployer of the recipe collection
  I want "npm run build" to produce a static "dist" directory
  So that Vercel can serve the recipe box and recipe pages

  Background:
    Given "scripts/build-site.sh" is the implementation of "npm run build"
    And "vercel.json" sets "buildCommand" to "npm run build" and "outputDirectory" to "dist"
    And committed static files exist under "recipe-system/web/" including "recipe-box.html"

  Scenario: npm build copies the static site into dist
    When I run "npm run build" from the repository root
    Then a "dist" directory is created
    And "dist/recipe-box.html" exists
    And the build prints that the static site is ready in "dist"

  Scenario: Prefer regenerating HTML when Python and lxml are available
    Given python3 and the lxml package are available
    When I run "npm run build" from the repository root
    Then "recipe-gen.py" and "cookbook-pkg.py" run before files are copied to "dist"
    And "dist" contains the regenerated recipe-box and recipe pages

  Scenario: Fall back to committed static files when lxml is unavailable
    Given python3 is available but lxml cannot be imported
    When I run "npm run build" from the repository root
    Then the build warns that lxml is not available
    And committed files under "recipe-system/web/" are still copied to "dist"

  Scenario: Vercel serves the recipe box at the site root
    Given a successful build with "dist/recipe-box.html"
    When Vercel deploys using repository-root "vercel.json"
    Then requests to "/" are rewritten to "/recipe-box.html"
