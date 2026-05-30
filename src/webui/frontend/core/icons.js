// Inline SVG loader. Fetches an icon once, caches the markup, and returns a
// detached <span class="icon"> whose inner <svg> uses stroke="currentColor",
// so every icon inherits the active theme color.

const cache = new Map();

async function rawSvg(name) {
  if (!cache.has(name)) {
    cache.set(
      name,
      fetch(`/resources/icons/${name}.svg`)
        .then((r) => (r.ok ? r.text() : ""))
        .catch(() => "")
    );
  }
  return cache.get(name);
}

export async function iconEl(name) {
  const span = document.createElement("span");
  span.className = "icon";
  span.innerHTML = await rawSvg(name);
  return span;
}

// Replace every <span data-icon="name"> inside root with its inline SVG.
export async function hydrateIcons(root) {
  const targets = root.querySelectorAll("[data-icon]");
  await Promise.all(
    [...targets].map(async (el) => {
      el.classList.add("icon");
      el.innerHTML = await rawSvg(el.dataset.icon);
    })
  );
}

export const icons = { iconEl, hydrateIcons };
