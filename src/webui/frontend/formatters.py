from __future__ import annotations


def format_prediction(result: dict) -> str:
    prediction = result.get("prediction") or {}
    label = prediction.get("label")
    probs = prediction.get("probabilities") or {}
    return (
        f"标签: {label}\n"
        f"非谣言概率: {float(probs.get('0', probs.get(0, 0.0))):.4f}\n"
        f"谣言概率: {float(probs.get('1', probs.get(1, 0.0))):.4f}\n"
        f"模型: {prediction.get('model_name', '')}"
    )


def format_cases(result: dict) -> str:
    cases = result.get("similar_cases") or []
    lines = []
    for case in cases:
        lines.append(f"- [{case.get('label')}, {case.get('score', 0):.3f}] {case.get('text')}")
    return "\n".join(lines) if lines else "无"

