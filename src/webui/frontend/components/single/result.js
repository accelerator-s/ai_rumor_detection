import { labelName } from "../../core/api.js";

function prob(probs, key) {
  if (!probs) return 0;
  return Number(probs[key] ?? probs[String(key)] ?? 0);
}

// Renders the classification result: an SVG confidence donut + dual probability
// bars + meta. Themed by verdict (rumor red / safe green).
export function renderResult(host, payload) {
  const pred = (payload.result && payload.result.prediction) || {};
  const probs = pred.probabilities || {};
  const p0 = prob(probs, 0);
  const p1 = prob(probs, 1);
  const isRumor = pred.label === 1;
  const confidence = Math.max(p0, p1);
  const tone = isRumor ? "is-rumor" : "is-safe";

  const R = 52;
  const C = 2 * Math.PI * R;

  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="result"></span><h2>预测结果</h2>
      </div>
      <div class="single-result card ${tone}">
        <div class="single-result__donut">
          <svg viewBox="0 0 130 130" class="single-result__ring">
            <circle class="single-result__track-ring" cx="65" cy="65" r="${R}" />
            <circle class="single-result__value-ring" cx="65" cy="65" r="${R}"
              stroke-dasharray="${C}" stroke-dashoffset="${C}" data-ring
              transform="rotate(-90 65 65)" />
            <text x="65" y="60" class="single-result__pct">${(confidence * 100).toFixed(0)}%</text>
            <text x="65" y="80" class="single-result__pct-sub">置信度</text>
          </svg>
          <span class="single-result__badge ${tone}">${labelName(pred.label)}</span>
        </div>

        <div class="single-result__bars">
          <div class="single-result__bar">
            <div class="single-result__bar-head">
              <span>非谣言 (0)</span><span class="value">${(p0 * 100).toFixed(2)}%</span>
            </div>
            <div class="single-result__track"><div class="single-result__fill is-safe" data-fill="0"></div></div>
          </div>
          <div class="single-result__bar">
            <div class="single-result__bar-head">
              <span>谣言 (1)</span><span class="value">${(p1 * 100).toFixed(2)}%</span>
            </div>
            <div class="single-result__track"><div class="single-result__fill is-rumor" data-fill="1"></div></div>
          </div>

          <div class="single-result__meta">
            <span>模型 <b>${escapeHtml(pred.model_name || "—")}</b></span>
            <span>耗时 <b>${payload.elapsedMs ?? "—"} ms</b></span>
            <span>模式 <b>${payload.mode === "explain" ? "检测+解释" : "仅分类"}</b></span>
          </div>
        </div>
      </div>
    </section>
  `;

  requestAnimationFrame(() => {
    const ring = host.querySelector("[data-ring]");
    if (ring) ring.style.strokeDashoffset = String(C * (1 - confidence));
    host.querySelector('[data-fill="0"]').style.width = `${(p0 * 100).toFixed(2)}%`;
    host.querySelector('[data-fill="1"]').style.width = `${(p1 * 100).toFixed(2)}%`;
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);
}
