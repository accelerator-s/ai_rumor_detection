import { classifierReady, explanationReady, getHealth } from "../../core/health.js";
import { hydrateIcons } from "../../core/icons.js";
import { renderState } from "../state-card/state-card.js";
import { createStepper } from "../stepper/stepper.js";
import { renderCases } from "./cases.js";
import { renderEvidence } from "./evidence.js";
import { mountExport } from "./export.js";
import { mountInput } from "./input.js";
import { renderResult } from "./result.js";

const STEPS = [
  { id: "input", label: "输入文本", hint: "选择检测方式" },
  { id: "result", label: "分类结果", hint: "标签与置信度" },
  { id: "evidence", label: "解释依据", hint: "文本证据" },
  { id: "cases", label: "相似案例", hint: "训练集参考" },
  { id: "export", label: "导出结果", hint: "保存或重测" },
];

function scrollToStep(host) {
  host?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function scrollToTop(root) {
  root?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export async function mount(root, ctx) {
  const hosts = Object.fromEntries(
    [...root.querySelectorAll("[data-step-host]")].map((el) => [el.dataset.stepHost, el])
  );
  const stepper = await createStepper(root.querySelector("[data-stepper]"), STEPS);
  let latest = null;

  const input = mountInput(hosts.input, ctx, { onRun: run });
  const output = mountExport(hosts.export, {
    onRerun: (payload) => run(payload.mode, payload.text, payload.event),
    onClear: clear,
  });

  await reset();

  async function reset() {
    latest = null;
    stepper.reset();
    stepper.set("input", "active");
    hosts.evidence.innerHTML = "";
    hosts.cases.innerHTML = "";
    output.clear();
    await renderState(hosts.result, {
      kind: "empty",
      title: "等待检测",
      detail: "输入一条文本，分类结果、依据和相似案例会在这里依次展开。",
    });
  }

  async function clear() {
    input.setText("");
    input.setEvent(null);
    await reset();
    scrollToTop(root);
  }

  async function run(mode, text, event) {
    if (!text) {
      stepper.set("input", "error");
      await renderState(hosts.result, {
        kind: "error",
        title: "请输入文本",
        detail: "粘贴一条推文或选择示例文本后再运行检测。",
      });
      return;
    }
    const normalizedEvent = String(event || "").trim();
    if (!normalizedEvent) {
      stepper.set("input", "error");
      await renderState(hosts.result, {
        kind: "error",
        title: "请输入事件编号",
        detail: "最终模型需要 event 特征。请填写事件编号后再运行检测。",
      });
      return;
    }
    const ready = mode === "explain" ? explanationReady() : classifierReady();
    if (!ready) {
      const health = getHealth();
      const classifierOk = classifierReady();
      stepper.set("input", "error");
      await renderState(hosts.result, {
        kind: "error",
        title: classifierOk ? "解释配置未完成" : "模型未加载",
        detail: classifierOk
          ? "请先在“大模型配置”页面补全服务地址、访问密钥和解释模型。"
          : (health && health.error) || "分类模型尚未加载，暂时无法运行检测。",
      });
      return;
    }

    input.setBusy(true, mode);
    hosts.evidence.innerHTML = "";
    hosts.cases.innerHTML = "";
    output.clear();
    stepper.reset();
    stepper.set("input", "done");
    stepper.set("result", "active");
    await renderState(hosts.result, {
      kind: "loading",
      title: mode === "explain" ? "正在检测并生成解释" : "正在分类",
      detail: "请稍候，完成后将自动展示后续步骤。",
    });
    scrollToStep(hosts.result);

    const started = performance.now();
    try {
      const result = mode === "explain" ? await ctx.api.explain(text, normalizedEvent) : await ctx.api.predict(text, normalizedEvent);
      input.remember(text, normalizedEvent);
      const payload = { result, mode, text, event: normalizedEvent, elapsedMs: Math.round(performance.now() - started) };
      latest = payload;

      renderResult(hosts.result, payload);
      await hydrateIcons(hosts.result);
      scrollToStep(hosts.result);
      stepper.set("result", "done");
      stepper.set("evidence", "active");

      renderEvidence(hosts.evidence, payload);
      await hydrateIcons(hosts.evidence);
      scrollToStep(hosts.evidence);
      stepper.set("evidence", "done");
      stepper.set("cases", "active");

      await renderCases(hosts.cases, payload);
      scrollToStep(hosts.cases);
      stepper.set("cases", "done");
      stepper.set("export", "active");

      await output.setPayload(payload);
      scrollToStep(hosts.export);
      stepper.set("export", "done");
      ctx.bus.emit("result", payload);
    } catch (err) {
      const message = err.message || "检测失败";
      stepper.set("result", "error");
      await renderState(hosts.result, {
        kind: "error",
        title: "检测失败",
        detail: message,
        retry: () => run(mode, text, event),
      });
      ctx.bus.emit("result-error", message);
    } finally {
      input.setBusy(false, mode);
    }
  }
}
