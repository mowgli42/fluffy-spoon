Feature: Offline recipe and meal-plan access
  As a cook who already opened Fluffy Spoon online
  I want recipes, the current week plan, and BBQ prep offline
  So that kitchen use does not depend on Wi-Fi

  # ---------------------------------------------------------------------------
  # @validated — Playwright offline E2E + static Vercel/build path
  # ---------------------------------------------------------------------------

  @validated @offline-viewing @vercel
  Scenario: Vercel demo needs no local backend for viewing
    Given the production Vercel deployment of the PWA shell
    When a visitor opens the recipe list and a sample meal-plan week
    Then content loads from static or seeded assets
    And no FastAPI or SQLite process is required on the visitor machine

  @validated @offline-viewing
  Scenario: Offline shell after first visit
    Given the user has loaded the demo once while online
    And the service worker has precached the app shell and seed data
    When the network is offline
    And the user reloads the start URL
    Then the app shell and seeded recipe list still render

  @validated @offline-viewing
  Scenario: View a saved recipe while offline
    Given the user has previously opened a recipe while online
    When the device is offline
    And the user navigates to that recipe
    Then the ingredients and instructions are displayed from local storage
    # Images: seed has no photos yet; UI states that text/steps are cached

  @validated @offline-viewing
  Scenario: View current week meal plan offline
    Given a 52-week plan seed has been loaded into the client store
    When the user opens the current week view offline
    Then the planned meals and BBQ prep items are visible
