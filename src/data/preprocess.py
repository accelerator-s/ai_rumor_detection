from __future__ import annotations

import html
import re

import emoji


URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
# Do not match the domain portion of an email address as a Twitter handle.
USER_RE = re.compile(r"(?<![\w@])@\w+")
RT_RE = re.compile(r"^\s*rt\s+", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")
EMOJI_TOKEN_RE = re.compile(r":([a-z0-9_\-&+]+):")


def _normalize_emoji(text: str) -> str:
    return emoji.demojize(text, language="en", delimiters=(" ", " "))


def normalize_text(text: str, emoji_normalization: bool = True) -> str:
    text = html.unescape(str(text))
    if emoji_normalization:
        text = _normalize_emoji(text)
    text = RT_RE.sub("", text)
    text = URL_RE.sub("HTTPURL", text)
    text = USER_RE.sub("@USER", text)
    text = EMOJI_TOKEN_RE.sub(lambda match: f"{match.group(1).replace('_', ' ')}", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def make_text_view(text: str, normalized: bool = True) -> str:
    return normalize_text(text) if normalized else str(text).strip()
