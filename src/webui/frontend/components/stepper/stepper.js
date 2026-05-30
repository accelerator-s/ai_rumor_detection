import { iconEl } from "../../core/icons.js";

// Reusable vertical stepper. Renders a column of step nodes (dot + connector +
// label) into `host` and exposes set()/reset() so a workflow can light steps up
// as it advances. States: idle | active | done | error. `active` breathes,
// `done` shows a check, `error` pulses red.
//
// createStepper(host, [{ id, label, hint? }, ...]) -> { set, reset, get, el }

const STATES = ["idle", "active", "done", "error"];

export async function createStepper(host, steps) {
  host.classList.add("stepper");
  host.innerHTML = "";

  const nodes = new Map();
  const check = await checkMarkup();

  steps.forEach((step, i) => {
    const item = document.createElement("div");
    item.className = "stepper__item is-idle";
    item.dataset.step = step.id;

    const rail = document.createElement("div");
    rail.className = "stepper__rail";

    const dot = document.createElement("span");
    dot.className = "stepper__dot";
    dot.innerHTML = `<span class="stepper__num">${i + 1}</span><span class="stepper__check">${check}</span>`;
    rail.append(dot);

    if (i < steps.length - 1) {
      const line = document.createElement("span");
      line.className = "stepper__line";
      rail.append(line);
    }

    const body = document.createElement("div");
    body.className = "stepper__body";
    const label = document.createElement("div");
    label.className = "stepper__label";
    label.textContent = step.label;
    body.append(label);
    if (step.hint) {
      const hint = document.createElement("div");
      hint.className = "stepper__hint";
      hint.textContent = step.hint;
      body.append(hint);
    }

    item.append(rail, body);
    host.append(item);
    nodes.set(step.id, item);
  });

  function set(id, state) {
    const item = nodes.get(id);
    if (!item || !STATES.includes(state)) return;
    STATES.forEach((s) => item.classList.toggle(`is-${s}`, s === state));
  }

  function get(id) {
    const item = nodes.get(id);
    if (!item) return null;
    return STATES.find((s) => item.classList.contains(`is-${s}`)) || "idle";
  }

  function reset() {
    for (const id of nodes.keys()) set(id, "idle");
  }

  return { set, get, reset, el: host };
}

async function checkMarkup() {
  const span = await iconEl("check");
  return span.innerHTML;
}
