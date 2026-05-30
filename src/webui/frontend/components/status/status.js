import { hydrateIcons } from "../../core/icons.js";

const RING_RADIUS = 48;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

export async function mount(root, ctx) {
  await hydrateIcons(root);

  const readinessRing = root.querySelector("[data-readiness-ring]");
  const readinessValue = root.querySelector("[data-readiness-value]");
  const backendState = root.querySelector("[data-backend-state]");
  const classifierState = root.querySelector("[data-classifier-state]");
  const explainState = root.querySelector("[data-explain-state]");
  const backendBar = root.querySelector("[data-backend-bar]");
  const classifierBar = root.querySelector("[data-classifier-bar]");
  const explainBar = root.querySelector("[data-explain-bar]");
  const llmModel = root.querySelector("[data-llm-model]");
  const llmBase = root.querySelector("[data-llm-base]");
  const llmKey = root.querySelector("[data-llm-key]");
  const llmTemp = root.querySelector("[data-llm-temp]");
  const diagnostic = root.querySelector("[data-diagnostic]");

  readinessRing.style.strokeDasharray = `${RING_CIRCUMFERENCE}`;
  readinessRing.style.strokeDashoffset = `${RING_CIRCUMFERENCE}`;

  ctx.bus.on("health", updateHealth);

  function updateHealth(data) {
    const reachable = data != null;
    const llm = data?.llm || {};
    const classifierReady = Boolean(reachable && data.classifier_ready);
    const llmReady = Boolean(reachable && llm.base_url && llm.model && llm.has_api_key);
    const allReady = Boolean(reachable && classifierReady && llmReady);
    const readiness = [reachable, classifierReady, llmReady].filter(Boolean).length / 3;
    const state = !reachable || !classifierReady ? "bad" : allReady ? "ok" : "warn";

    readinessRing.dataset.state = state;
    readinessRing.style.strokeDashoffset = `${RING_CIRCUMFERENCE * (1 - readiness)}`;
    readinessValue.textContent = `${Math.round(readiness * 100)}%`;

    setMetric(backendState, backendBar, reachable, "已连接", "不可达");
    setMetric(classifierState, classifierBar, classifierReady, "已加载", "未加载");
    setMetric(explainState, explainBar, llmReady, "已配置", "未完成");

    llmModel.textContent = llm.model || "未配置";
    llmBase.textContent = llm.base_url || "未配置";
    llmKey.textContent = llm.has_api_key ? "已保存" : "未配置";
    llmTemp.textContent = llm.temperature ?? "—";

    diagnostic.dataset.state = state;
    diagnostic.textContent = diagnosticText({ reachable, classifierReady, llmReady, allReady, error: data?.error });
  }

  function setMetric(label, bar, active, positiveText, negativeText) {
    label.textContent = active ? positiveText : negativeText;
    label.dataset.state = active ? "ok" : "bad";
    bar.style.width = active ? "100%" : "28%";
    bar.dataset.state = active ? "ok" : "bad";
  }

  function diagnosticText({ reachable, classifierReady, llmReady, allReady, error }) {
    if (!reachable) {
      return "后端健康检查没有返回结果。请确认服务进程、端口和浏览器访问地址是否一致。";
    }
    if (allReady) {
      return "当前服务链路完整：分类权重已加载，解释模型接入参数已配置，可进行单条检测、检测并解释和批量评测。";
    }
    if (!classifierReady) {
      return error || "后端已响应，但分类权重尚未加载。请先完成训练并确认 checkpoint 文件完整。";
    }
    if (!llmReady) {
      return "分类链路已就绪，批量评测不受影响；如需生成解释，请在大模型配置页补全服务地址、访问密钥和模型。";
    }
    return "服务状态已更新。";
  }
}
