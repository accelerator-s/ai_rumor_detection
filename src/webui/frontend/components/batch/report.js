import { hydrateIcons } from "../../core/icons.js";

export function mountReport(host, { onRerun, onClear }) {
  let latest = null;
  let filename = "";

  async function setReport(data, sourceName) {
    latest = data;
    filename = sourceName;
    host.innerHTML = `
      <section class="workflow-section">
        <div class="workflow-section__head">
          <span class="icon" data-icon="download"></span><h2>保存报告</h2>
        </div>
        <div class="batch-report card">
          <span>已完成 ${data.count} 条分类，可保存本次批量评测报告。</span>
          <button class="btn btn--primary" type="button" data-download>
            <span class="icon" data-icon="download"></span>下载 JSON 报告
          </button>
          <button class="btn" type="button" data-rerun>重新评测</button>
          <button class="btn btn--ghost" type="button" data-clear>清空结果</button>
        </div>
      </section>`;
    await hydrateIcons(host);
    host.querySelector("[data-download]").addEventListener("click", download);
    host.querySelector("[data-rerun]").addEventListener("click", () => onRerun());
    host.querySelector("[data-clear]").addEventListener("click", onClear);
  }

  function download() {
    if (!latest) return;
    const report = JSON.stringify({ filename, ...latest }, null, 2);
    const url = URL.createObjectURL(new Blob([report], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `rumor-batch-report-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function clear() {
    latest = null;
    filename = "";
    host.innerHTML = "";
  }

  return { setReport, clear };
}
