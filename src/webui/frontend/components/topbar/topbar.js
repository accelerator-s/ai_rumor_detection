import { iconEl } from "../../core/icons.js";
import { toggleTheme, currentTheme, onThemeChange } from "../../core/theme.js";

const TITLES = {
  single: { title: "单条检测", sub: "输入文本 → 结果 → 依据 → 相似案例", icon: "detect" },
  batch: { title: "批量评测", sub: "导入 CSV，评估自训练模型分类的准确率", icon: "batch" },
  config: {
    title: "大模型配置",
    sub: "设置解释模型的服务地址、访问密钥和模型种类，OpenAI 兼容接口。",
    icon: "robot",
  },
  status: {
    title: "服务状态",
    sub: "查看后端连接、分类模型与解释配置的实时就绪情况。",
    icon: "status",
  },
};

export async function mount(root, ctx) {
  const titleEl = root.querySelector("[data-title]");
  const subEl = root.querySelector("[data-sub]");
  const pageIcon = root.querySelector("[data-page-icon]");
  const themeBtn = root.querySelector("[data-theme-toggle]");
  const health = root.querySelector("[data-health]");
  const healthText = root.querySelector("[data-health-text]");

  async function setPageIcon(name) {
    pageIcon.innerHTML = "";
    const ic = await iconEl(name);
    ic.classList.add("topbar__page-icon");
    pageIcon.append(ic);
  }
  async function setThemeIcon() {
    themeBtn.innerHTML = "";
    const ic = await iconEl(currentTheme() === "dark" ? "theme-sun" : "theme-moon");
    themeBtn.append(ic);
  }
  await setThemeIcon();
  await setPageIcon(TITLES.single.icon);
  themeBtn.addEventListener("click", () => {
    toggleTheme();
  });
  onThemeChange(setThemeIcon);

  ctx.bus.on("route", async (id) => {
    const meta = TITLES[id] || TITLES.single;
    titleEl.textContent = meta.title;
    subEl.textContent = meta.sub;
    await setPageIcon(meta.icon);
  });

  function setHealth(data) {
    const reachable = data != null;
    const llm = data?.llm || {};
    const classifierReady = Boolean(reachable && data.classifier_ready);
    const llmReady = Boolean(reachable && llm.base_url && llm.model && llm.has_api_key);
    const allReady = Boolean(reachable && classifierReady && llmReady);
    const cls = !reachable ? "is-off" : allReady ? "is-ok" : "is-bad";
    health.classList.remove("is-ok", "is-bad", "is-off", "is-unknown");
    health.classList.add(cls);
    if (!reachable) {
      healthText.textContent = "服务不可达";
      health.title = "后端连接不可达，请确认服务进程和访问地址";
    } else if (allReady) {
      healthText.textContent = "服务正常";
      health.title = "后端连接、分类模型接入与解释模型接入均已就绪";
    } else if (!classifierReady) {
      healthText.textContent = "分类模型未接入";
      health.title = (data && data.error) || "后端已连接，分类模型接入未完成";
    } else {
      healthText.textContent = "解释模型未接入";
      health.title = "分类模型已接入，解释模型接入参数尚未补全";
    }
  }
  ctx.bus.on("health", setHealth);
}
