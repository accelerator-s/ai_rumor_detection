// Thin fetch wrappers over the backend JSON API. No business logic here —
// just transport + label mapping the backend leaves to the client.

export const LABEL_NAMES = { 0: "非谣言", 1: "谣言" };

export function labelName(label) {
  return LABEL_NAMES[label] ?? String(label ?? "");
}

async function request(method, path, body) {
  const opts = { method, headers: {} };
  if (body !== undefined) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }
  if (!res.ok) {
    const message = (data && data.error) || `请求失败 (${res.status})`;
    throw new Error(message);
  }
  return data;
}

export const api = {
  health: () => request("GET", "/health"),
  predict: (text, event) => request("POST", "/predict", { text, event }),
  explain: (text, event) => request("POST", "/explain", { text, event }),
  batch: (content, filename) => request("POST", "/batch", { content, filename }),
  llmConfig: () => request("GET", "/llm/config"),
  saveLlmConfig: (payload) => request("POST", "/llm/config", payload),
  llmModels: (base_url, api_key) =>
    request("POST", "/llm/models", { base_url, api_key }),
  llmTest: (payload) => request("POST", "/llm/test", payload),
};
