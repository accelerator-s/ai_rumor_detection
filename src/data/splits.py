from __future__ import annotations

import random
from collections import defaultdict
from typing import Iterable

from src.data.dataset import RumorExample


def group_by_event(examples: Iterable[RumorExample]) -> dict[str, list[RumorExample]]:
    groups: dict[str, list[RumorExample]] = defaultdict(list)
    for example in examples:
        groups[example.event].append(example)
    return dict(groups)


def event_holdout_split(
    examples: list[RumorExample],
    valid_ratio: float = 0.2,
    seed: int = 42,
) -> tuple[list[RumorExample], list[RumorExample]]:
    events = sorted(group_by_event(examples))
    rng = random.Random(seed)
    rng.shuffle(events)
    valid_count = max(1, int(len(events) * valid_ratio))
    valid_events = set(events[:valid_count])
    train = [item for item in examples if item.event not in valid_events]
    valid = [item for item in examples if item.event in valid_events]
    return train, valid

