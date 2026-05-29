from __future__ import annotations

from src.data.preprocess import normalize_text


def simple_evidence(text: str, limit: int = 8) -> list[tuple[str, float]]:
    tokens = [token for token in normalize_text(text).split(" ") if len(token) > 2]
    seen: set[str] = set()
    scored: list[tuple[str, float]] = []
    for token in tokens:
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        score = min(1.0, len(token) / 16)
        scored.append((token, score))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:limit]

