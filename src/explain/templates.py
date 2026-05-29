from __future__ import annotations

from src.interfaces import Prediction, SimilarCase


def format_cases(cases: list[SimilarCase]) -> str:
    if not cases:
        return "无"
    lines = []
    for case in cases:
        lines.append(f"- [{case.label_name}, event={case.event}, score={case.score:.3f}] {case.text}")
    return "\n".join(lines)


def format_evidence(evidence: list[tuple[str, float]]) -> str:
    if not evidence:
        return "无"
    return "\n".join(f"- {token}: {score:.3f}" for token, score in evidence)


def build_prompt(template: str, text: str, prediction: Prediction, evidence, cases) -> str:
    return template.format(
        text=text,
        label_name=prediction.label_name,
        confidence=prediction.confidence,
        evidence=format_evidence(evidence),
        cases=format_cases(cases),
    )

