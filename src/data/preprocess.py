from __future__ import annotations

import html
import re

import emoji


URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
USER_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_]+)")
RT_RE = re.compile(r"^\s*rt\s+", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")
EMOJI_TOKEN_RE = re.compile(r":([a-z0-9_\-&+]+):")
SOURCE_MENTION_ALLOWLIST = {
    "9newsaus",
    "9newssyd",
    "abc",
    "abcnews",
    "afp",
    "ap",
    "bbcbreaking",
    "bbcworld",
    "cbcnews",
    "cbcottawa",
    "cnn",
    "cp24",
    "ctvnews",
    "ctvottawa",
    "dailytelegraph",
    "europe1",
    "flightcrisis",
    "flightradar24",
    "fox2now",
    "germanwings",
    "globeandmail",
    "grahamctv",
    "kmov",
    "ksdknews",
    "kunstmuseumbern",
    "livenationon",
    "lufthansa",
    "lufthansa_de",
    "masseyhall",
    "nbcnews",
    "nswpolice",
    "nytimes",
    "ottawahospital",
    "ottawapolice",
    "patthomas",
    "pmharper",
    "pmonair",
    "rcmp_nat_div",
    "rcmpgrcpolice",
    "rideaucentre",
    "reuters",
    "smh",
    "skybusiness",
    "stlcountypd",
    "swissinfo_en",
    "thetorontostar",
    "torontostar",
    "worldnews",
}


def _normalize_emoji(text: str) -> str:
    return emoji.demojize(text, language="en", delimiters=(":", ":"))


def _normalize_mention(match: re.Match[str]) -> str:
    username = match.group(1)
    return match.group(0) if username.lower() in SOURCE_MENTION_ALLOWLIST else "@USER"


def normalize_text(text: str, emoji_normalization: bool = True) -> str:
    text = html.unescape(str(text))
    text = RT_RE.sub("", text)
    text = URL_RE.sub("HTTPURL", text)
    text = USER_RE.sub(_normalize_mention, text)
    if emoji_normalization:
        text = _normalize_emoji(text)
        text = EMOJI_TOKEN_RE.sub(lambda match: f" {match.group(1).replace('_', ' ')} ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def make_text_view(text: str, normalized: bool = True) -> str:
    return normalize_text(text) if normalized else str(text).strip()
