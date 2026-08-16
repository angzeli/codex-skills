(function () {
  "use strict";

  var root = document.documentElement;
  var storageKey = "mira-vale-theme";

  function storedTheme() {
    try {
      var value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (error) {
      return null;
    }
  }

  function preferredTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme, button) {
    var isDark = theme === "dark";
    root.dataset.theme = theme;

    if (button) {
      button.setAttribute("aria-pressed", String(isDark));
      button.setAttribute("aria-label", "Switch to " + (isDark ? "light" : "dark") + " theme");
      button.querySelector("[data-theme-label]").textContent = isDark ? "Light" : "Dark";
      button.querySelector("[data-theme-icon]").textContent = isDark ? "☀" : "◐";
    }
  }

  var initialTheme = storedTheme() || preferredTheme();
  applyTheme(initialTheme);

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    applyTheme(root.dataset.theme || initialTheme, button);

    button.addEventListener("click", function () {
      var nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(nextTheme, button);

      try {
        window.localStorage.setItem(storageKey, nextTheme);
      } catch (error) {
        // The visible theme still changes when storage is unavailable.
      }
    });
  });
})();
