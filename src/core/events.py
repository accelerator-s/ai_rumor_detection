from __future__ import annotations

VALID_EVENTS = frozenset(str(index) for index in range(7))
VALID_EVENT_TEXT = "0, 1, 2, 3, 4, 5, 6"


class EventInputError(ValueError):
    pass


def normalize_event(event: str | int | None) -> str:
    value = str(event or "").strip()
    if not value:
        raise EventInputError("请输入事件编号。")
    if value not in VALID_EVENTS:
        raise EventInputError(f"事件编号必须是 {VALID_EVENT_TEXT} 之一。")
    return value
