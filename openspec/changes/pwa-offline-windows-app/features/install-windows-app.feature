Feature: Install and run Fluffy Spoon as a Windows app
  As a household cook on Windows
  I want Fluffy Spoon installed like a normal app
  So that I can open meal plans without browser chrome

  # ---------------------------------------------------------------------------
  # @prototype — intended for the Svelte+Vite PWA slice (not yet exercised)
  # ---------------------------------------------------------------------------

  @prototype @pwa-install
  Scenario: Manifest makes the site installable
    Given the demo is served over HTTPS on Vercel or localhost
    When a client fetches the web app manifest
    Then the manifest name is "Fluffy Spoon"
    And display is "standalone"
    And start_url and theme colors are present
    And icons suitable for install are listed

  # ---------------------------------------------------------------------------
  # @aspirational — requires real Windows Edge/Chrome install; manual proof
  # ---------------------------------------------------------------------------

  @aspirational @pwa-install
  Scenario: User installs the site as a Windows app
    Given the site is open in Microsoft Edge or Chrome
    And the PWA installability criteria are met
    When the user chooses "Install this site as an app"
    Then the app appears in the Start menu
    And launching it opens a standalone window with no browser UI

  @aspirational @pwa-install @offline
  Scenario: App launches offline after install
    Given the app has been installed and the user has previously loaded recipes
    When the device has no internet connection
    And the user launches the Fluffy Spoon app
    Then the main meal-plan and recipe views still render from cache
