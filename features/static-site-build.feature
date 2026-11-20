Feature: Build static site output for Vercel
  As a deployer of the recipe collection
  I want "npm run build" to produce a static "dist" directory
  So that Vercel can serve the Fluffy Spoon PWA and classic recipe box

  Background:
    Given "scripts/build-site.sh" is the implementation of "npm run build"
    And "vercel.json" sets "buildCommand" to "npm run build" and "outputDirectory" to "dist"
    And committed static files exist under "recipe-system/web/" including "recipe-box.html"
    And the Svelte PWA lives under "pwa/"

  Scenario: npm build produces PWA index and classic recipe box
    When I run "npm run build" from the repository root
    Then a "dist" directory is created
    And "dist/index.html" exists
    And "dist/classic/recipe-box.html" exists
    And "dist/data/seed.json" exists
    And the build prints that the site is ready in "dist"

  Scenario: Prefer regenerating HTML when Python and lxml are available
    Given python3 and the lxml package are available
    When I run "npm run build" from the repository root
    Then "recipe-gen.py" and "cookbook-pkg.py" run before classic files are copied to "dist/classic"
    And "export-pwa-seed.py" writes "pwa/public/data/seed.json"

  Scenario: Fall back to committed static files when lxml is unavailable
    Given python3 is available but lxml cannot be imported
    When I run "npm run build" from the repository root
    Then the build warns that lxml is not available
    And committed files under "recipe-system/web/" are still copied to "dist/classic"

  Scenario: Vercel serves the PWA at the site root
    Given a successful build with "dist/index.html"
    When Vercel deploys using repository-root "vercel.json"
    Then requests to "/" serve the Fluffy Spoon PWA shell
    And "/classic" reaches the legacy recipe-box
