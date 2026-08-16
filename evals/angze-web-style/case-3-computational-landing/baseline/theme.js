(function () {
  "use strict";

  const storageKey = "tesserachem-theme";
  const root = document.documentElement;
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  function storedTheme() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (error) {
      return null;
    }
  }

  function saveTheme(theme) {
    try {
      window.localStorage.setItem(storageKey, theme);
    } catch (error) {
      // The selected theme still applies when browser storage is unavailable.
    }
  }

  function applyTheme(theme, button) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;

    if (!button) {
      return;
    }

    const nextTheme = theme === "dark" ? "light" : "dark";
    const stateLabel = button.querySelector("[data-theme-state]");

    button.setAttribute("aria-pressed", String(theme === "dark"));
    button.setAttribute("aria-label", `Switch to ${nextTheme} theme`);

    if (stateLabel) {
      stateLabel.textContent = theme === "dark" ? "Dark" : "Light";
    }
  }

  const initialTheme = storedTheme() || (mediaQuery.matches ? "dark" : "light");
  applyTheme(initialTheme);

  document.addEventListener("DOMContentLoaded", function () {
    const button = document.querySelector("[data-theme-toggle]");
    applyTheme(root.dataset.theme || initialTheme, button);

    if (button) {
      button.addEventListener("click", function () {
        const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
        applyTheme(nextTheme, button);
        saveTheme(nextTheme);
      });
    }

    mediaQuery.addEventListener("change", function (event) {
      if (!storedTheme()) {
        applyTheme(event.matches ? "dark" : "light", button);
      }
    });
  });
})();
