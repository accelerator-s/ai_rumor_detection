import {
  classifierReady,
  explanationReady,
  getHealth,
  onHealth,
} from "../../core/health.js";

const DEFAULT_HISTORY = [
  {
    text: "So, to sum up: 1) Darren Wilson KNEW NOTHING of the robbery, 2) shot #MikeBrown over jaywalking, and 3) was allowed to escape #Ferguson.",
    event: "1",
  },
  {
    text: "BREAKING: #Ferguson police chief just announced that officer Darren Wilson shot the unarmed teen, Michael Brown.",
    event: "1",
  },
  {
    text: "so ... they clearly released that video  only to shame &amp; blame the victim. #Ferguson #MikeBrown",
    event: "1",
  },
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

      <label class="field-label" for="single-event">事件编号</label>
      <select class="input single-input__event" id="single-event">
        <option value="">请选择事件编号</option>
        <option value="0">Event 0 · Gurlitt art collection</option>
        <option value="1">Event 1 · Ferguson and Michael Brown</option>
        <option value="2">Event 2 · Michael Essien and Ebola</option>
        <option value="3">Event 3 · Prince Toronto concert</option>
        <option value="4">Event 4 · Germanwings crash</option>
        <option value="5">Event 5 · Sydney cafe siege</option>
        <option value="6">Event 6 · Ottawa shooting</option>
      </select>

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
  const event = host.querySelector(".single-input__event");
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
      const entry = normalizeHistoryEntry(item);
      if (!entry.text) {
        continue;
      }
      const key = `${entry.event}\n${entry.text}`;
      if (seen.has(key)) {
        continue;
      }
      seen.add(key);
      out.push(entry);
      if (out.length === HISTORY_LIMIT) {
        break;
      }
    }
    for (const item of DEFAULT_HISTORY) {
      if (out.length === HISTORY_LIMIT) {
        break;
      }
      const entry = normalizeHistoryEntry(item);
      const key = `${entry.event}\n${entry.text}`;
      if (!seen.has(key)) {
        seen.add(key);
        out.push(entry);
      }
    }
    return out;
  }

  function normalizeHistoryEntry(item) {
    if (item && typeof item === "object") {
      return {
        text: String(item.text || "").trim(),
        event: String(item.event || "").trim(),
      };
    }
    return { text: String(item || "").trim(), event: "" };
  }

  let history = loadHistory();

  function renderHistory() {
    examplesBox.innerHTML = "";
    for (const ex of history) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "single-input__example";
      btn.textContent = ex.event ? `event ${ex.event} · ${ex.text}` : ex.text;
      btn.title = ex.event ? `event ${ex.event}\n${ex.text}` : ex.text;
      btn.addEventListener("click", () => {
        text.value = ex.text;
        event.value = ex.event;
        text.focus();
      });
      examplesBox.append(btn);
    }
  }

  function remember(value, eventValue = null) {
    const normalized = String(value || "").trim();
    if (!normalized) {
      return;
    }
    history = normalizeHistory([{ text: normalized, event: String(eventValue || "").trim() }, ...history]);
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

  predictBtn.addEventListener("click", () => onRun("predict", text.value.trim(), event.value.trim()));
  explainBtn.addEventListener("click", () => onRun("explain", text.value.trim(), event.value.trim()));
  text.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && explanationReady()) {
      onRun("explain", text.value.trim(), event.value.trim());
    }
  });

  return {
    getText: () => text.value.trim(),
    getEvent: () => event.value.trim(),
    setText: (v) => {
      text.value = v;
    },
    setEvent: (v) => {
      event.value = v || "";
    },
    remember,
    setBusy,
  };
}
