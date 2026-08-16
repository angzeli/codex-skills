(function () {
  "use strict";

  var root = document.documentElement;
  var storageKey = "mira-vale-archive-theme";
  var systemQuery = window.matchMedia("(prefers-color-scheme: dark)");
  var themeMeta = document.querySelector('meta[name="theme-color"]');
  var manualChoice = readStoredChoice();

  function readStoredChoice() {
    try {
      var choice = window.localStorage.getItem(storageKey);
      return choice === "light" || choice === "dark" ? choice : null;
    } catch (error) {
      return null;
    }
  }

  function systemChoice() {
    return systemQuery.matches ? "dark" : "light";
  }

  function syncControls(theme) {
    document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
      var isActive = button.dataset.themeChoice === theme;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    if (themeMeta) {
      themeMeta.setAttribute("content", theme === "dark" ? "#11181d" : "#f5efe4");
    }
    syncControls(theme);
  }

  applyTheme(manualChoice || systemChoice());

  document.addEventListener("DOMContentLoaded", function () {
    themeMeta = document.querySelector('meta[name="theme-color"]');
    applyTheme(root.dataset.theme || manualChoice || systemChoice());

    document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
      button.addEventListener("click", function () {
        var choice = button.dataset.themeChoice;
        if (choice !== "light" && choice !== "dark") return;

        manualChoice = choice;
        applyTheme(choice);

        try {
          window.localStorage.setItem(storageKey, choice);
        } catch (error) {
          // The choice remains active for this page when storage is unavailable.
        }
      });
    });
  });

  systemQuery.addEventListener("change", function () {
    if (manualChoice === null) applyTheme(systemChoice());
  });
})();
