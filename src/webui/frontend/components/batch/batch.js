import { hydrateIcons } from "../../core/icons.js";
import { renderState } from "../state-card/state-card.js";
import { createStepper } from "../stepper/stepper.js";
import { renderCharts } from "./charts.js";
import { renderMetrics } from "./metrics.js";
import { mountReport } from "./report.js";
import { renderTable } from "./table.js";
import { mountUpload } from "./upload.js";

const STEPS = [
  { id: "upload", label: "导入 CSV", hint: "选择评测文件" },
  { id: "run", label: "批量分类", hint: "不提供检索与 LLM" },
  { id: "metrics", label: "评测指标", hint: "指标与混淆矩阵" },
  { id: "charts", label: "分布图表", hint: "标签与预测分布" },
  { id: "table", label: "预测明细", hint: "检查错误样本" },
  { id: "report", label: "保存报告", hint: "下载 JSON" },
];

export async function mount(root, ctx) {
  const hosts = Object.fromEntries(
    [...root.querySelectorAll("[data-batch-host]")].map((el) => [el.dataset.batchHost, el])
  );
  const stepper = await createStepper(root.querySelector("[data-stepper]"), STEPS);
  let latestInput = null;
  const upload = await mountUpload(hosts.upload, { onRun: run });
  const report = mountReport(hosts.report, {
    onRerun: () => latestInput && run(latestInput),
    onClear: clear,
  });
  await reset();

  async function reset() {
    stepper.reset();
    stepper.set("upload", "active");
    hosts.charts.innerHTML = "";
    hosts.table.innerHTML = "";
    report.clear();
    await renderState(hosts.metrics, {
      kind: "empty",
      title: "等待批量评测",
      detail: "导入 CSV 后运行评测，这里将展示指标、分布图表和预测明细。",
    });
  }

  function clear() {
    void reset();
  }

  async function run(input) {
    if (input.error) {
      await renderState(hosts.metrics, {
        kind: "error",
        title: "读取文件失败",
        detail: input.error,
      });
      return;
    }
    latestInput = input;
    upload.setBusy(true);
    stepper.reset();
    stepper.set("upload", "done");
    stepper.set("run", "active");
    hosts.charts.innerHTML = "";
    hosts.table.innerHTML = "";
    report.clear();
    await renderState(hosts.metrics, {
      kind: "loading",
      title: "正在运行批量分类",
      detail: "仅调用本地分类模型，不调用检索或大模型解释。",
    });

    try {
      const data = await ctx.api.batch(input.content, input.filename);
      stepper.set("run", "done");
      stepper.set("metrics", "active");
      renderMetrics(hosts.metrics, data);
      await hydrateIcons(hosts.metrics);
      stepper.set("metrics", "done");

      stepper.set("charts", "active");
      renderCharts(hosts.charts, data);
      await hydrateIcons(hosts.charts);
      stepper.set("charts", "done");

      stepper.set("table", "active");
      renderTable(hosts.table, data);
      await hydrateIcons(hosts.table);
      stepper.set("table", "done");

      stepper.set("report", "active");
      await report.setReport(data, input.filename);
      stepper.set("report", "done");
      ctx.bus.emit("batch-result", data);
    } catch (err) {
      const message = err.message || "批量评测失败";
      stepper.set("run", "error");
      await renderState(hosts.metrics, {
        kind: "error",
        title: "批量评测失败",
        detail: message,
        retry: () => run(input),
      });
    } finally {
      upload.setBusy(false);
    }
  }
}
