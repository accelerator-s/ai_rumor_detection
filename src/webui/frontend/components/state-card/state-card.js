import { iconEl } from "../../core/icons.js";

const KINDS = {
  empty: { icon: "doc", cls: "state-card--empty" },
  loading: { icon: "spark", cls: "state-card--loading" },
  error: { icon: "alert", cls: "state-card--error" },
};

// Renders a themed empty / loading / error placeholder into `host`, replacing
// bare `<p class="empty">` text so failure and progress states look intentional.
export async function renderState(host, { kind = "empty", title = "", detail = "", retry } = {}) {
  const spec = KINDS[kind] || KINDS.empty;
  host.innerHTML = "";

  const card = document.createElement("div");
  card.className = `state-card ${spec.cls}`;

  const icon = await iconEl(spec.icon);
  icon.classList.add("state-card__icon");
  card.append(icon);

  if (kind === "loading") {
    const bar = document.createElement("div");
    bar.className = "state-card__shimmer";
    card.append(bar);
  }

  if (title) {
    const h = document.createElement("p");
    h.className = "state-card__title";
    h.textContent = title;
    card.append(h);
  }

  if (detail) {
    const d = document.createElement("p");
    d.className = "state-card__detail";
    d.textContent = detail;
    card.append(d);
  }

  if (typeof retry === "function") {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn state-card__retry";
    btn.textContent = "重试";
    btn.addEventListener("click", retry);
    card.append(btn);
  }

  host.append(card);
  return card;
}
