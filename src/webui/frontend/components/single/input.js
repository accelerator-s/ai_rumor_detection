import {
  classifierReady,
  explanationReady,
  getHealth,
  onHealth,
} from "../../core/health.js";

const DEFAULT_HISTORY = [
  '#Ferguson PD beat, &amp; charged innocent man with "Property Damage" for bleeding on officer\'s clothes @YourAnonNews http://t.co/cdyvEIzZRw',
  "BREAKING: Officials confirm the missing flight has been found intact, all passengers safe.",
  "RT @user: They are saying the earthquake was predicted weeks ago and nobody warned us 😢",
];
const HISTORY_KEY = "rumor.single.inputHistory";
const HISTORY_LIMIT = 3;

// Builds the input step. Calls onRun(mode, text) when a button is pressed.
// Returns { getText, setBusy } so single.js can drive busy state during a run.
export function mountInput(host, ctx, { onRun }) {
  host.innerHTML = `
    <div class="single-input card">
      <label class="field-label" for="single-text">推文 / 文本</label>
      <textarea class="textarea single-input__text" id="single-text"
        placeholder="粘贴一条推文或一段文本，然后选择检测方式…"></textarea>

      <div class="single-input__history-head">
        <span>历史记录</span>
        <small>检测成功后会保留最近 3 条，点击即可填入文本框。</small>
      </div>
      <div class="single-input__examples" data-examples></div>

      <div class="single-input__gate" data-gate hidden></div>

      <div class="single-input__actions">
        <button class="btn" data-action="predict" type="button">仅分类</button>
        <button class="btn btn--primary" data-action="explain" type="button">检测并解释</button>
        <span class="single-input__busy" data-busy hidden>
          <span class="spinner"></span><span data-busy-text>分类中…</span>
        </span>
      </div>
    </div>
  `;

  const text = host.querySelector(".single-input__text");
  const examplesBox = host.querySelector("[data-examples]");
  const busy = host.querySelector("[data-busy]");
  const busyText = host.querySelector("[data-busy-text]");
  const gate = host.querySelector("[data-gate]");
  const predictBtn = host.querySelector('[data-action="predict"]');
  const explainBtn = host.querySelector('[data-action="explain"]');
  const actionBtns = [predictBtn, explainBtn];

  function loadHistory() {
    try {
      const parsed = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
      if (Array.isArray(parsed)) {
        return normalizeHistory(parsed);
      }
    } catch (err) {
      localStorage.removeItem(HISTORY_KEY);
    }
    return [...DEFAULT_HISTORY];
  }

  function saveHistory(next) {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
  }

  function normalizeHistory(items) {
    const seen = new Set();
    const out = [];
    for (const item of items) {
      const value = String(item || "").trim();
      if (!value || seen.has(value)) {
        continue;
      }
      seen.add(value);
      out.push(value);
      if (out.length === HISTORY_LIMIT) {
        break;
      }
    }
    for (const item of DEFAULT_HISTORY) {
      if (out.length === HISTORY_LIMIT) {
        break;
      }
      if (!seen.has(item)) {
        seen.add(item);
        out.push(item);
      }
    }
    return out;
  }

  let history = loadHistory();

  function renderHistory() {
    examplesBox.innerHTML = "";
    for (const ex of history) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "single-input__example";
      btn.textContent = ex;
      btn.title = ex;
      btn.addEventListener("click", () => {
        text.value = ex;
        text.focus();
      });
      examplesBox.append(btn);
    }
  }

  function remember(value) {
    const normalized = String(value || "").trim();
    if (!normalized) {
      return;
    }
    history = normalizeHistory([normalized, ...history]);
    saveHistory(history);
    renderHistory();
  }

  renderHistory();

  let busyOn = false;

  function applyGate(health = getHealth()) {
    const classifierOk = classifierReady();
    const explanationOk = explanationReady();
    gate.hidden = classifierOk && explanationOk;
    gate.classList.toggle("is-warn", classifierOk && !explanationOk);
    gate.textContent = classifierOk && explanationOk
      ? ""
      : health === undefined
        ? "正在检查后端模型状态…"
        : health === null
          ? "后端服务不可达，暂时无法检测。"
          : classifierOk
            ? "分类功能可用。如需生成解释，请先在“大模型配置”页面补全服务地址、访问密钥和解释模型。"
            : health.error || "分类模型尚未加载，暂时无法检测。";
    predictBtn.disabled = busyOn || !classifierOk;
    explainBtn.disabled = busyOn || !explanationOk;
  }

  // Health-driven pre-flight gating: disable buttons when not ready so we never
  // fire a request that is doomed to hang.
  onHealth(applyGate);
  applyGate();

  function setBusy(on, mode) {
    busyOn = on;
    busy.hidden = !on;
    busyText.textContent = mode === "explain" ? "检测并生成解释中…" : "分类中…";
    applyGate();
  }

  predictBtn.addEventListener("click", () => onRun("predict", text.value.trim()));
  explainBtn.addEventListener("click", () => onRun("explain", text.value.trim()));
  text.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && explanationReady()) {
      onRun("explain", text.value.trim());
    }
  });

  return {
    getText: () => text.value.trim(),
    setText: (v) => {
      text.value = v;
    },
    remember,
    setBusy,
  };
}
