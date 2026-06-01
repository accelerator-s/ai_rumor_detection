import { labelName } from "../../core/api.js";

const MAX_VISIBLE_ROWS = 100;

export function renderTable(host, data) {
  const rows = (data.rows || []).slice(0, MAX_VISIBLE_ROWS);
  const body = rows.map((row) => `
    <tr class="${row.correct === false ? "is-wrong" : ""}">
      <td>${escapeHtml(row.id)}</td>
      <td>${escapeHtml(row.event)}</td>
      <td title="${escapeHtml(row.text)}">${escapeHtml(row.text)}</td>
      <td>${row.label == null ? "—" : labelName(row.label)}</td>
      <td>${labelName(row.pred)}</td>
      <td>${(Number(row.prob1 || 0) * 100).toFixed(2)}%</td>
    </tr>`).join("");
  const shown = Math.min(rows.length, MAX_VISIBLE_ROWS);

  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="table"></span><h2>预测明细</h2>
      </div>
      <p class="workflow-section__sub">展示前 ${shown} 条明细，预测错误行以红色标记。</p>
      <div class="batch-table card">
        <table>
          <thead><tr><th>ID</th><th>Event</th><th>文本</th><th>真实标签</th><th>预测标签</th><th>谣言概率</th></tr></thead>
          <tbody>${body}</tbody>
        </table>
      </div>
    </section>`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);
}
