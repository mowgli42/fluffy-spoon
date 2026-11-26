Feature: Offline writes and sync
  As a cook marking meals done in the kitchen
  I want offline changes kept and synced later
  So that I do not lose progress when Wi-Fi drops

  # ---------------------------------------------------------------------------
  # @aspirational — no write API in the viewing prototype; production rebuild
  # ---------------------------------------------------------------------------

  @aspirational @offline-sync @future
  Scenario: Changes made offline are queued
    Given the user marks a meal as cooked while offline
    When connectivity returns
    Then the change is synced to the backend
    And the local queue entry is cleared on success

  @aspirational @offline-sync @future
  Scenario: Sync conflict is resolved per production policy
    Given the same meal was updated on another device while this device was offline
    When the offline queue syncs
    Then the client applies the documented conflict policy
    And the user can see the resulting cooked state
