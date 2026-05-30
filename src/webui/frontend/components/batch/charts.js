const R = 42;
const C = 2 * Math.PI * R;

function donut(title, dist) {
  const safe = Number(dist[0] || 0);
  const rumor = Number(dist[1] || 0);
  const total = safe + rumor;
  const rumorRatio = total ? rumor / total : 0;
  return `
    <div class="batch-chart card">
      <h3>${title}</h3>
      <div class="batch-chart__body">
        <svg viewBox="0 0 112 112">
          <circle class="batch-chart__track" cx="56" cy="56" r="${R}" />
          <circle class="batch-chart__ring" cx="56" cy="56" r="${R}"
            stroke-dasharray="${C}" stroke-dashoffset="${C}" data-offset="${C * (1 - rumorRatio)}"
            transform="rotate(-90 56 56)" />
          <text x="56" y="53">${total}</text>
          <text class="batch-chart__sub" x="56" y="69">样本</text>
        </svg>
        <div class="batch-chart__legend">
          <span><i class="is-safe"></i>非谣言 <b>${safe}</b></span>
          <span><i class="is-rumor"></i>谣言 <b>${rumor}</b></span>
        </div>
      </div>
    </div>`;
}

export function renderCharts(host, data) {
  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="chart"></span><h2>分布图表</h2>
      </div>
      <div class="batch-charts">
        ${donut("真实标签分布", data.label_dist || {})}
        ${donut("预测标签分布", data.pred_dist || {})}
      </div>
    </section>`;
  requestAnimationFrame(() => {
    host.querySelectorAll("[data-offset]").forEach((ring) => {
      ring.style.strokeDashoffset = ring.dataset.offset;
    });
  });
}
