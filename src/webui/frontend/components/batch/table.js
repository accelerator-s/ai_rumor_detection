import { labelName } from "../../core/api.js";
import { hydrateIcons } from "../../core/icons.js";

const PAGE_SIZE = 20;
const WRONG_ONLY_KEY = "rumor.batch.table.showWrongOnly";

export function renderTable(host, data) {
  const allRows = data.rows || [];
  const wrongRows = allRows.filter((row) => row.correct === false);
  let page = 1;
  let showWrongOnly = loadWrongOnlyPreference();

  function currentRows() {
    return showWrongOnly ? wrongRows : allRows;
  }

  function render() {
    const activeRows = currentRows();
    const totalPages = Math.max(1, Math.ceil(activeRows.length / PAGE_SIZE));
    page = Math.min(page, totalPages);
    const start = (page - 1) * PAGE_SIZE;
    const rows = activeRows.slice(start, start + PAGE_SIZE);
    const body = rows.map((row) => `
      <tr class="${row.correct === false ? "is-wrong" : ""}">
        <td>${escapeHtml(row.id)}</td>
        <td>${escapeHtml(row.event)}</td>
        <td title="${escapeHtml(row.text)}">${escapeHtml(row.text)}</td>
        <td>${row.label == null ? "—" : labelName(row.label)}</td>
        <td>${labelName(row.pred)}</td>
        <td>${(Number(row.prob1 || 0) * 100).toFixed(2)}%</td>
      </tr>`).join("");
    const summary = showWrongOnly
      ? `仅展示判断错误的结果，共 ${wrongRows.length} 条，每页 ${PAGE_SIZE} 条。`
      : `展示全部检测结果，共 ${allRows.length} 条，其中错误结果 ${wrongRows.length} 条，每页 ${PAGE_SIZE} 条。`;
    const pager = activeRows.length
      ? `
        <div class="batch-table__pager">
          <button class="btn btn--ghost" type="button" data-page="prev" ${page === 1 ? "disabled" : ""}>上一页</button>
          <span class="batch-table__pager-text">第 ${page} / ${totalPages} 页</span>
          <button class="btn btn--ghost" type="button" data-page="next" ${page === totalPages ? "disabled" : ""}>下一页</button>
        </div>`
      : "";

    host.innerHTML = `
      <section class="workflow-section">
        <div class="workflow-section__head">
          <span class="icon" data-icon="table"></span><h2>检测结果</h2>
        </div>
        <div class="batch-table__toolbar">
          <label class="batch-table__toggle" for="batch-table-wrong-only">
            <input id="batch-table-wrong-only" type="checkbox" data-toggle ${showWrongOnly ? "checked" : ""} />
            <span class="batch-table__toggle-label">仅错误结果</span>
          </label>
          <p class="workflow-section__sub">${summary}</p>
        </div>
        <div class="batch-table card">
          ${activeRows.length
            ? `
              <table>
                <thead><tr><th>ID</th><th>Event</th><th>文本</th><th>真实标签</th><th>预测标签</th><th>谣言概率</th></tr></thead>
                <tbody>${body}</tbody>
              </table>`
            : `<span class="empty">${showWrongOnly ? "本次批量检测没有判断错误的结果。" : "本次批量检测没有可展示的结果。"}</span>`}
        </div>
        ${pager}
      </section>`;

    hydrateIcons(host);

    const toggle = host.querySelector("[data-toggle]");
    const prev = host.querySelector('[data-page="prev"]');
    const next = host.querySelector('[data-page="next"]');

    toggle?.addEventListener("change", () => {
      showWrongOnly = toggle.checked;
      saveWrongOnlyPreference(showWrongOnly);
      page = 1;
      render();
    });
    prev?.addEventListener("click", () => {
      if (page <= 1) return;
      page -= 1;
      render();
    });
    next?.addEventListener("click", () => {
      if (page >= totalPages) return;
      page += 1;
      render();
    });
  }

  render();
}

function loadWrongOnlyPreference() {
  try {
    return localStorage.getItem(WRONG_ONLY_KEY) === "true";
  } catch (err) {
    return false;
  }
}

function saveWrongOnlyPreference(value) {
  try {
    localStorage.setItem(WRONG_ONLY_KEY, value ? "true" : "false");
  } catch (err) {
    // ignore storage failures
  }
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
