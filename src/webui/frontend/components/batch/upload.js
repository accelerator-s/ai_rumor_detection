import { classifierReady, getHealth, onHealth } from "../../core/health.js";
import { hydrateIcons } from "../../core/icons.js";

export async function mountUpload(host, { onRun }) {
  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="upload"></span><h2>导入 CSV</h2>
      </div>
      <div class="batch-upload card">
        <label class="batch-upload__drop" for="batch-file">
          <span class="icon" data-icon="upload"></span>
          <strong>选择 CSV 文件</strong>
          <span>需包含 text 列；存在 label 列时计算 Accuracy、Precision、Recall 和 F1。</span>
          <input id="batch-file" type="file" accept=".csv,text/csv" />
        </label>
        <p class="batch-upload__file" data-file>尚未选择文件</p>
        <p class="batch-upload__note">批量评测仅调用分类模型，不会调用检索或大模型解释接口。</p>
        <p class="batch-upload__gate" data-gate hidden></p>
        <div class="batch-upload__actions">
          <button class="btn btn--primary" type="button" data-run disabled>
            <span class="icon" data-icon="chart"></span>运行评测
          </button>
          <span class="batch-upload__busy" data-busy hidden>
            <span class="spinner"></span><span>正在逐条分类…</span>
          </span>
        </div>
      </div>
    </section>`;
  await hydrateIcons(host);

  const input = host.querySelector("#batch-file");
  const runBtn = host.querySelector("[data-run]");
  const busy = host.querySelector("[data-busy]");
  const gate = host.querySelector("[data-gate]");
  const fileInfo = host.querySelector("[data-file]");
  let selected = null;
  let busyOn = false;

  function gateText(health) {
    if (health === undefined) return "正在检查后端模型状态…";
    if (health === null) return "后端服务不可达，暂时无法运行评测。";
    return health.error || "分类模型尚未加载，暂时无法运行评测。";
  }

  function updateGate(health = getHealth()) {
    const ready = classifierReady();
    gate.hidden = ready;
    gate.textContent = ready ? "" : gateText(health);
    runBtn.disabled = busyOn || !ready || !selected;
  }

  onHealth(updateGate);
  updateGate();

  input.addEventListener("change", () => {
    selected = input.files && input.files[0] ? input.files[0] : null;
    fileInfo.textContent = selected
      ? `${selected.name} · ${(selected.size / 1024).toFixed(1)} KB`
      : "尚未选择文件";
    updateGate();
  });

  runBtn.addEventListener("click", () => {
    if (!selected || !classifierReady()) return;
    const reader = new FileReader();
    reader.addEventListener("load", () => onRun({
      filename: selected.name,
      content: String(reader.result || ""),
    }));
    reader.addEventListener("error", () => onRun({
      filename: selected.name,
      error: "无法读取所选 CSV 文件。",
    }));
    reader.readAsText(selected, "utf-8");
  });

  function setBusy(on) {
    busyOn = on;
    busy.hidden = !on;
    input.disabled = on;
    updateGate();
  }

  return { setBusy };
}
