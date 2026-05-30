// Caches the latest health payload from the bus so workflow panes can gate
// actions without each maintaining their own polling loop.
let current = undefined;
const listeners = new Set();

export function initHealth(bus) {
  bus.on("health", (data) => {
    current = data;
    listeners.forEach((fn) => fn(data));
  });
}

export function getHealth() {
  return current;
}

export function classifierReady() {
  return Boolean(current && (current.classifier_ready ?? current.ok) === true);
}

export function explanationReady() {
  return Boolean(current && (current.explanation_ready ?? current.ok) === true);
}

export function onHealth(fn) {
  listeners.add(fn);
  if (current !== undefined) fn(current);
  return () => listeners.delete(fn);
}
