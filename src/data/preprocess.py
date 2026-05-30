from __future__ import annotations

import html
import re


URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
# Do not match the domain portion of an email address as a Twitter handle.
USER_RE = re.compile(r"(?<![\w@])@\w+")
RT_RE = re.compile(r"^\s*rt\s+", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    text = html.unescape(str(text))
    text = RT_RE.sub("", text)
    text = URL_RE.sub("HTTPURL", text)
    text = USER_RE.sub("@USER", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def make_text_view(text: str, normalized: bool = True) -> str:
    return normalize_text(text) if normalized else str(text).strip()
