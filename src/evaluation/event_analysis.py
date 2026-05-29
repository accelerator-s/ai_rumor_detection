from __future__ import annotations

from collections import defaultdict

from src.data.dataset import RumorExample
from src.evaluation.metrics import binary_metrics


def metrics_by_event(
    examples: list[RumorExample],
    predictions: list[int],
) -> dict[str, dict[str, float]]:
    grouped_true: dict[str, list[int]] = defaultdict(list)
    grouped_pred: dict[str, list[int]] = defaultdict(list)

    for example, pred in zip(examples, predictions):
        grouped_true[example.event].append(int(example.label))
        grouped_pred[example.event].append(int(pred))

    return {
        event: binary_metrics(grouped_true[event], grouped_pred[event])
        for event in sorted(grouped_true)
    }

