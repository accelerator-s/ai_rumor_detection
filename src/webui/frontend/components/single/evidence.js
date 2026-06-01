import { renderAiMessage } from "../../core/ai_output.js";

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);
}

function chipColor(weight, maxAbs) {
  if (!maxAbs) return "var(--surface-2)";
  const ratio = Math.min(1, Math.abs(weight) / maxAbs);
  const token = weight >= 0 ? "--rumor" : "--safe";
  return `color-mix(in srgb, var(${token}) ${Math.round(ratio * 48)}%, var(--surface-2))`;
}

export function renderEvidence(host, payload) {
  const result = payload.result || {};
  const explanation = result.explanation || null;
  const evidence = (explanation && explanation.evidence) || result.evidence || [];
  const maxAbs = evidence.reduce((max, [, weight]) => Math.max(max, Math.abs(Number(weight) || 0)), 0);
  const reason = explanation && explanation.text
    ? explanation.text
    : "本次为仅分类模式，未调用大模型生成自然语言解释。模型证据仍展示如下。";
  const chips = evidence.map(([token, weight], index) => {
    const score = Number(weight) || 0;
    return `
      <span class="single-evidence__chip" style="background:${chipColor(score, maxAbs)};animation-delay:${index * 24}ms">
        ${escapeHtml(token)}<span>${score >= 0 ? "+" : ""}${score.toFixed(2)}</span>
      </span>`;
  }).join("");

  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="explain"></span><h2>解释依据</h2>
      </div>
      <div class="single-evidence card">
        <div class="single-evidence__reason" data-reason></div>
        <div class="single-evidence__head">关键证据词（${evidence.length}）</div>
        <div class="single-evidence__chips">${chips || '<span class="empty">无可展示的证据词。</span>'}</div>
      </div>
    </section>`;

  renderAiMessage(host.querySelector("[data-reason]"), reason);
}
