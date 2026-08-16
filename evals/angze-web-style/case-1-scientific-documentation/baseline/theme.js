(function () {
  "use strict";

  const storageKey = "moleculum-theme";
  const root = document.documentElement;
  const toggle = document.querySelector(".theme-toggle");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  function readPreference() {
    try {
      return localStorage.getItem(storageKey);
    } catch (_error) {
      return null;
    }
  }

  function savePreference(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (_error) {
      // The selected theme still applies for this page view when storage is unavailable.
    }
  }

  function preferredTheme() {
    const storedTheme = readPreference();
    if (storedTheme === "light" || storedTheme === "dark") {
      return storedTheme;
    }
    return systemTheme.matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (toggle) {
      const isDark = theme === "dark";
      toggle.setAttribute("aria-pressed", String(isDark));
      toggle.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} theme`);
      toggle.title = `Switch to ${isDark ? "light" : "dark"} theme`;
    }
  }

  applyTheme(preferredTheme());

  if (toggle) {
    toggle.addEventListener("click", function () {
      const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
      savePreference(nextTheme);
    });
  }

  systemTheme.addEventListener("change", function (event) {
    if (!readPreference()) {
      applyTheme(event.matches ? "dark" : "light");
    }
  });
})();
