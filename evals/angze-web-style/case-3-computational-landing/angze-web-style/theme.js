(function () {
  "use strict";

  const storageKey = "tesserachem-theme";
  const root = document.documentElement;
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  const themeColors = {
    light: "#f2efe8",
    dark: "#11181d"
  };

  root.classList.add("js");

  function readStoredTheme() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (error) {
      return null;
    }
  }

  function writeStoredTheme(theme) {
    try {
      window.localStorage.setItem(storageKey, theme);
    } catch (error) {
      // The active theme remains usable when storage is unavailable.
    }
  }

  function updateControls(theme) {
    document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
      const isActive = button.dataset.themeChoice === theme;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function updateThemeColor(theme) {
    const meta = document.querySelector("[data-theme-color]");
    if (meta) {
      meta.setAttribute("content", themeColors[theme]);
    }
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    updateThemeColor(theme);
    updateControls(theme);
  }

  const initialTheme = readStoredTheme() || (systemTheme.matches ? "dark" : "light");
  applyTheme(initialTheme);

  document.addEventListener("DOMContentLoaded", function () {
    updateControls(root.dataset.theme || initialTheme);

    document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
      button.addEventListener("click", function () {
        const theme = button.dataset.themeChoice;
        if (theme === "light" || theme === "dark") {
          applyTheme(theme);
          writeStoredTheme(theme);
        }
      });
    });
  });

  systemTheme.addEventListener("change", function (event) {
    if (!readStoredTheme()) {
      applyTheme(event.matches ? "dark" : "light");
    }
  });
})();
