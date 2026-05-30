import { labelName } from "../../core/api.js";
import { hydrateIcons } from "../../core/icons.js";

export async function renderCases(host, payload) {
  const result = payload.result || {};
  const cases = result.similar_cases || (result.explanation && result.explanation.cases) || [];
  const items = cases.map((item, index) => {
    const rumor = item.label === 1;
    return `
      <article class="single-cases__item" style="animation-delay:${index * 42}ms">
        <div class="single-cases__meta">
          <span class="single-cases__badge ${rumor ? "is-rumor" : "is-safe"}">${labelName(item.label)}</span>
          ${item.event ? `<span>${escapeHtml(item.event)}</span>` : ""}
          <b>相似度 ${(Number(item.score || 0) * 100).toFixed(1)}%</b>
        </div>
        <p>${escapeHtml(item.text || "")}</p>
      </article>`;
  }).join("");

  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="cases"></span><h2>相似案例</h2>
      </div>
      <p class="workflow-section__sub">来自训练集的 Top-K 相似样本，仅作为参考。</p>
      <div class="single-cases">${items || '<div class="card single-cases__empty">未检索到相似案例。</div>'}</div>
    </section>`;
  await hydrateIcons(host);
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
