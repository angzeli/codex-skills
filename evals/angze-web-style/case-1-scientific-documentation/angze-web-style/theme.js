(function () {
  "use strict";

  const storageKey = "moleculum-documentation-theme";
  const root = document.documentElement;
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  const themeColors = {
    light: "#f2efe8",
    dark: "#11181d"
  };

  function isValidTheme(value) {
    return value === "light" || value === "dark";
  }

  function readStoredTheme() {
    try {
      const value = localStorage.getItem(storageKey);
      return isValidTheme(value) ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function storeTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (_error) {
      // The explicit choice remains active for this page view.
    }
  }

  function systemChoice() {
    return systemTheme.matches ? "dark" : "light";
  }

  let storedTheme = readStoredTheme();
  let hasManualChoice = storedTheme !== null;
  let activeTheme = storedTheme || systemChoice();

  function updateThemeColor(theme) {
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", themeColors[theme]);
    }
  }

  function syncControls(theme) {
    const controls = document.querySelectorAll("[data-theme-choice]");
    controls.forEach(function (control) {
      const isActive = control.dataset.themeChoice === theme;
      control.classList.toggle("is-active", isActive);
      control.setAttribute("aria-pressed", String(isActive));
    });
  }

  function applyTheme(theme) {
    activeTheme = theme;
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    updateThemeColor(theme);
    syncControls(theme);
  }

  applyTheme(activeTheme);

  function initializeControls() {
    syncControls(activeTheme);
    document.querySelectorAll("[data-theme-choice]").forEach(function (control) {
      control.addEventListener("click", function () {
        const choice = control.dataset.themeChoice;
        if (!isValidTheme(choice)) {
          return;
        }

        hasManualChoice = true;
        storedTheme = choice;
        applyTheme(choice);
        storeTheme(choice);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeControls, { once: true });
  } else {
    initializeControls();
  }

  function followSystemTheme() {
    if (!hasManualChoice) {
      applyTheme(systemChoice());
    }
  }

  if (typeof systemTheme.addEventListener === "function") {
    systemTheme.addEventListener("change", followSystemTheme);
  } else if (typeof systemTheme.addListener === "function") {
    systemTheme.addListener(followSystemTheme);
  }
})();
