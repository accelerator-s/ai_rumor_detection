import { hydrateIcons } from "../../core/icons.js";
import { renderAiMessage } from "../../core/ai_output.js";
import { createSelect } from "./select.js";

const TEMP_KEY = "rumor-llm-temperature";
const MODEL_CACHE_KEY = "rumor-llm-model-cache";

export async function mount(root, ctx) {
  await hydrateIcons(root);

  const base = root.querySelector("#cfg-base");
  const key = root.querySelector("#cfg-key");
  const model = root.querySelector("#cfg-model");
  const modelSelect = createSelect(model);
  const temp = root.querySelector("#cfg-temp");
  const tempVal = root.querySelector("[data-temp-val]");
  const busy = root.querySelector("[data-busy]");
  const msg = root.querySelector("[data-msg]");
  const fetchBtn = root.querySelector('[data-action="fetch-models"]');
  const saveBtn = root.querySelector('[data-action="save"]');
  const testBtn = root.querySelector('[data-action="test"]');
  const testBusy = root.querySelector("[data-test-busy]");
  const testMsg = root.querySelector("[data-test-msg]");
  const testOut = root.querySelector("[data-test-out]");

  let savedBaseUrl = "";
  let savedHasApiKey = false;
  let lastCredentialSignature = "";
  let modelCache = { signature: "", models: [] };

  function currentBaseUrl() {
    return base.value.trim();
  }

  function savedCredentialSignature(baseUrl = currentBaseUrl()) {
    return `${baseUrl}\n__saved_api_key__`;
  }

  function draftCredentialSignature(baseUrl = currentBaseUrl()) {
    return `${baseUrl}\n__draft_api_key__`;
  }

  function hasSavedCredentialForCurrentBase() {
    const baseUrl = currentBaseUrl();
    return Boolean(baseUrl && savedHasApiKey && baseUrl === savedBaseUrl);
  }

  function hasAccessFields() {
    return Boolean(currentBaseUrl() && (key.value.trim() || hasSavedCredentialForCurrentBase()));
  }

  function credentialSignature() {
    const baseUrl = currentBaseUrl();
    if (!baseUrl) return "";
    if (key.value.trim()) return draftCredentialSignature(baseUrl);
    if (hasSavedCredentialForCurrentBase()) return savedCredentialSignature(baseUrl);
    return `${baseUrl}\n__missing_api_key__`;
  }

  function loadModelCache() {
    try {
      const cached = JSON.parse(localStorage.getItem(MODEL_CACHE_KEY) || "null");
      if (!cached || !Array.isArray(cached.models)) return { signature: "", models: [] };
      return {
        signature: String(cached.signature || ""),
        models: cached.models.map(String).filter(Boolean),
      };
    } catch {
      return { signature: "", models: [] };
    }
  }

  function saveModelCache(cache) {
    try {
      localStorage.setItem(MODEL_CACHE_KEY, JSON.stringify(cache));
    } catch {
      /* Browsers may disable local storage. */
    }
  }

  function clearModelCache() {
    modelCache = { signature: "", models: [] };
    try {
      localStorage.removeItem(MODEL_CACHE_KEY);
    } catch {
      /* Browsers may disable local storage. */
    }
  }

  function restoreCachedModels(selected) {
    if (modelCache.signature === lastCredentialSignature && modelCache.models.length) {
      setModels(modelCache.models, selected);
      return;
    }
    const draftSignature = draftCredentialSignature();
    if (
      hasSavedCredentialForCurrentBase() &&
      modelCache.signature === draftSignature &&
      modelCache.models.length
    ) {
      modelCache = { signature: lastCredentialSignature, models: modelCache.models };
      saveModelCache(modelCache);
      setModels(modelCache.models, selected);
    }
  }

  function refreshActionAvailability() {
    const ready = hasAccessFields();
    fetchBtn.disabled = !ready;
    testBtn.disabled = !ready;
    return ready;
  }

  function clearModelIfCredentialsChanged() {
    const next = credentialSignature();
    if (next !== lastCredentialSignature) {
      clearModelCache();
      modelSelect.setOptions([], "", "（先获取模型列表）");
      lastCredentialSignature = next;
    }
    refreshActionAvailability();
  }

  function requireAccessFields(show) {
    if (hasAccessFields()) return true;
    if (show) {
      show("请先填写服务地址和访问密钥", false);
    }
    refreshActionAvailability();
    return false;
  }

  function showMsg(text, ok) {
    msg.hidden = !text;
    msg.textContent = text || "";
    msg.className = `config__msg ${text ? (ok ? "is-ok" : "is-err") : ""}`;
  }

  function showTestMsg(text, ok) {
    testMsg.hidden = !text;
    testMsg.textContent = text || "";
    testMsg.className = `config__msg ${text ? (ok ? "is-ok" : "is-err") : ""}`;
  }

  function setModels(models, selected) {
    if (!models.length) {
      modelSelect.setOptions([], "", "（无可用模型）");
      return;
    }
    modelSelect.setOptions(models, selected);
  }

  function setTemperature(value, remember = false) {
    temp.value = value;
    tempVal.textContent = Number(temp.value).toFixed(1);
    if (!remember) return;
    try {
      localStorage.setItem(TEMP_KEY, temp.value);
    } catch {
      /* Browsers may disable local storage. */
    }
  }

  function rememberedTemperature() {
    try {
      return localStorage.getItem(TEMP_KEY);
    } catch {
      return null;
    }
  }

  temp.addEventListener("input", () => setTemperature(temp.value, true));
  base.addEventListener("input", refreshActionAvailability);
  key.addEventListener("input", refreshActionAvailability);
  base.addEventListener("blur", clearModelIfCredentialsChanged);
  key.addEventListener("blur", clearModelIfCredentialsChanged);

  try {
    const cfg = await ctx.api.llmConfig();
    base.value = cfg.base_url || "";
    savedBaseUrl = currentBaseUrl();
    savedHasApiKey = Boolean(cfg.has_api_key);
    setTemperature(rememberedTemperature() ?? cfg.temperature ?? 0.2);
    modelCache = loadModelCache();
    lastCredentialSignature = credentialSignature();
    restoreCachedModels(cfg.model || "");
    refreshActionAvailability();
  } catch (err) {
    showMsg(err.message || "读取配置失败", false);
  }

  fetchBtn.addEventListener("click", async () => {
    showMsg("", true);
    if (!requireAccessFields(showMsg)) return;
    const signature = credentialSignature();
    if (modelCache.signature === signature && modelCache.models.length) {
      setModels(modelCache.models, modelSelect.value);
      showMsg(`已使用前端缓存的 ${modelCache.models.length} 个模型`, true);
      return;
    }
    busy.hidden = false;
    fetchBtn.disabled = true;
    try {
      const data = await ctx.api.llmModels(currentBaseUrl(), key.value.trim());
      const models = data.models || [];
      modelCache = { signature, models };
      saveModelCache(modelCache);
      setModels(models, modelSelect.value);
      lastCredentialSignature = signature;
      showMsg(`获取到 ${models.length} 个模型`, true);
    } catch (err) {
      showMsg(err.message || "获取模型失败", false);
    } finally {
      busy.hidden = true;
      refreshActionAvailability();
    }
  });

  saveBtn.addEventListener("click", async () => {
    showMsg("", true);
    busy.hidden = false;
    saveBtn.disabled = true;
    const baseUrl = currentBaseUrl();
    const payload = {
      base_url: baseUrl,
      model: modelSelect.value,
      temperature: Number(temp.value),
    };
    const signatureBeforeSave = credentialSignature();
    if (key.value.trim()) payload.api_key = key.value.trim();
    try {
      await ctx.api.saveLlmConfig(payload);
      savedBaseUrl = baseUrl;
      savedHasApiKey = Boolean(payload.api_key || savedHasApiKey);
      key.value = "";
      const signatureAfterSave = credentialSignature();
      if (modelCache.signature === signatureBeforeSave && modelCache.models.length) {
        modelCache = { signature: signatureAfterSave, models: modelCache.models };
        saveModelCache(modelCache);
      }
      lastCredentialSignature = signatureAfterSave;
      refreshActionAvailability();
      showMsg("已保存", true);
      ctx.bus.emit("config-saved", payload);
    } catch (err) {
      showMsg(err.message || "保存失败", false);
    } finally {
      busy.hidden = true;
      saveBtn.disabled = false;
    }
  });

  testBtn.addEventListener("click", async () => {
    showTestMsg("", true);
    testOut.hidden = true;
    testOut.textContent = "";
    if (!requireAccessFields(showTestMsg)) return;
    testBusy.hidden = false;
    testBtn.disabled = true;
    const payload = {
      base_url: base.value.trim(),
      api_key: key.value.trim(),
      model: modelSelect.value,
      temperature: Number(temp.value),
    };
    try {
      const result = await ctx.api.llmTest(payload);
      renderAiMessage(testOut, result.message, { meta: `${result.elapsed_ms.toFixed(0)}ms · 模型响应` });
      testOut.hidden = false;
      showTestMsg("通讯成功", true);
    } catch (err) {
      showTestMsg(err.message || "通讯失败", false);
    } finally {
      testBusy.hidden = true;
      refreshActionAvailability();
    }
  });
}
