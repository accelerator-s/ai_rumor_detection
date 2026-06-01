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

function scrollToStep(host) {
  host?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

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
    hosts.upload.hidden = false;
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

  async function clear() {
    await reset();
    scrollToTop();
  }

  async function run(input) {
    if (input.error) {
      stepper.set("upload", "error");
      await renderState(hosts.metrics, {
        kind: "error",
        title: "读取文件失败",
        detail: input.error,
      });
      scrollToStep(hosts.metrics);
      return;
    }
    latestInput = input;
    upload.setBusy(true);
    hosts.upload.hidden = true;
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
    scrollToStep(hosts.metrics);

    try {
      const data = await ctx.api.batch(input.content, input.filename);

      renderMetrics(hosts.metrics, data);
      await hydrateIcons(hosts.metrics);
      stepper.set("run", "done");
      stepper.set("metrics", "active");
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
      hosts.upload.hidden = false;
      const message = err.message || "批量评测失败";
      if (stepper.get("run") === "active") {
        stepper.set("run", "error");
      } else if (stepper.get("metrics") === "active") {
        stepper.set("metrics", "error");
      } else if (stepper.get("charts") === "active") {
        stepper.set("charts", "error");
      } else if (stepper.get("table") === "active") {
        stepper.set("table", "error");
      } else if (stepper.get("report") === "active") {
        stepper.set("report", "error");
      } else {
        stepper.set("upload", "error");
      }
      await renderState(hosts.metrics, {
        kind: "error",
        title: "批量评测失败",
        detail: message,
        retry: () => run(input),
      });
      scrollToStep(hosts.metrics);
    } finally {
      upload.setBusy(false);
    }
  }
}
