import { hydrateIcons } from "../../core/icons.js";

export function mountExport(host, { onRerun, onClear }) {
  let latest = null;

  async function setPayload(payload) {
    latest = payload;
    host.innerHTML = `
      <section class="workflow-section">
        <div class="workflow-section__head">
          <span class="icon" data-icon="download"></span><h2>导出与重测</h2>
        </div>
        <div class="single-export card">
          <button class="btn btn--ghost" type="button" data-action="copy">
            <span class="icon" data-icon="copy"></span>复制 JSON
          </button>
          <button class="btn btn--ghost" type="button" data-action="download">
            <span class="icon" data-icon="download"></span>下载 JSON
          </button>
          <button class="btn" type="button" data-action="rerun">重新检测</button>
          <button class="btn btn--ghost" type="button" data-action="clear">清空</button>
          <span class="single-export__msg" data-msg></span>
        </div>
      </section>`;
    await hydrateIcons(host);

    const msg = host.querySelector("[data-msg]");
    host.querySelector('[data-action="copy"]').addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(serialized());
        msg.textContent = "已复制";
      } catch {
        msg.textContent = "浏览器拒绝剪贴板访问";
      }
    });
    host.querySelector('[data-action="download"]').addEventListener("click", download);
    host.querySelector('[data-action="rerun"]').addEventListener("click", () => onRerun(latest));
    host.querySelector('[data-action="clear"]').addEventListener("click", onClear);
  }

  function serialized() {
    return JSON.stringify(latest, null, 2);
  }

  function download() {
    if (!latest) return;
    const url = URL.createObjectURL(new Blob([serialized()], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `rumor-result-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function clear() {
    latest = null;
    host.innerHTML = "";
  }

  return { setPayload, clear };
}
