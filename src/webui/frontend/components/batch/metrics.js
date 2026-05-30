function pct(value) {
  return `${(Number(value || 0) * 100).toFixed(2)}%`;
}

export function renderMetrics(host, data) {
  const metrics = data.metrics || null;
  const confusion = data.confusion || null;
  const metricCards = metrics
    ? [
        ["Accuracy", metrics.accuracy],
        ["Precision", metrics.precision],
        ["Recall", metrics.recall],
        ["F1", metrics.f1],
      ].map(([name, value]) => `
        <div class="batch-metrics__metric card">
          <span>${name}</span><strong>${pct(value)}</strong>
        </div>`).join("")
    : '<div class="batch-metrics__notice card">CSV 未提供有效 label，已完成预测但不计算评测指标。</div>';
  const matrix = confusion ? `
    <div class="batch-metrics__matrix card">
      <h3>混淆矩阵</h3>
      <div class="batch-metrics__matrix-grid">
        <div><span>TN</span><strong>${confusion.tn}</strong></div>
        <div><span>FP</span><strong>${confusion.fp}</strong></div>
        <div><span>FN</span><strong>${confusion.fn}</strong></div>
        <div><span>TP</span><strong>${confusion.tp}</strong></div>
      </div>
    </div>` : "";

  host.innerHTML = `
    <section class="workflow-section">
      <div class="workflow-section__head">
        <span class="icon" data-icon="chart"></span><h2>评测指标</h2>
      </div>
      <p class="workflow-section__sub">共处理 ${data.count} 条，分类耗时 ${data.elapsed_ms} ms。</p>
      <div class="batch-metrics">
        <div class="batch-metrics__grid">${metricCards}</div>
        ${matrix}
      </div>
    </section>`;
}
