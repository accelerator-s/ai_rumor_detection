import { hydrateIcons, iconEl } from "../../core/icons.js";

const TABS = [
  { id: "status", label: "服务状态", icon: "status" },
  { id: "single", label: "单条检测", icon: "detect" },
  { id: "batch", label: "批量评测", icon: "batch" },
  { id: "config", label: "大模型配置", icon: "robot" },
];

export async function mount(root, ctx) {
  await hydrateIcons(root);
  const nav = root.querySelector("[data-tabs]");

  const buttons = new Map();
  for (const tab of TABS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "rail__tab";
    btn.dataset.tab = tab.id;
    btn.title = tab.label;
    btn.setAttribute("aria-label", tab.label);
    const ic = await iconEl(tab.icon);
    ic.classList.add("rail__tab-icon");
    btn.append(ic);
    const span = document.createElement("span");
    span.textContent = tab.label;
    btn.append(span);
    btn.addEventListener("click", () => ctx.bus.emit("route", tab.id));
    nav.append(btn);
    buttons.set(tab.id, btn);
  }

  ctx.bus.on("route", (id) => {
    for (const [tabId, btn] of buttons) {
      btn.classList.toggle("is-active", tabId === id);
    }
  });
}
