// Minimal pub/sub so components stay decoupled: detect emits "result",
// result/explain/cases subscribe; rail emits "route".

export function createBus() {
  const map = new Map();
  return {
    on(event, fn) {
      if (!map.has(event)) map.set(event, new Set());
      map.get(event).add(fn);
      return () => map.get(event)?.delete(fn);
    },
    emit(event, payload) {
      map.get(event)?.forEach((fn) => fn(payload));
    },
  };
}
