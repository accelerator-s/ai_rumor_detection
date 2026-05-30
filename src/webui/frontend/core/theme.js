// Theme state: read stored preference (or system), apply to <html data-theme>,
// toggle + persist. Components subscribe via onThemeChange to swap icons.

const KEY = "rumor-theme";
const listeners = new Set();

function systemPref() {
  return window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export function currentTheme() {
  return document.documentElement.dataset.theme || "light";
}

function apply(theme) {
  document.documentElement.dataset.theme = theme;
  listeners.forEach((fn) => fn(theme));
}

export function initTheme() {
  let stored = null;
  try {
    stored = localStorage.getItem(KEY);
  } catch {
    stored = null;
  }
  apply(stored || systemPref());
}

export function toggleTheme() {
  const next = currentTheme() === "dark" ? "light" : "dark";
  try {
    localStorage.setItem(KEY, next);
  } catch {
    /* ignore storage failure */
  }
  apply(next);
  return next;
}

export function onThemeChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}
