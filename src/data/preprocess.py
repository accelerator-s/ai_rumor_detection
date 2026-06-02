from __future__ import annotations

import html
import re

import emoji


URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
USER_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_]+)")
HASHTAG_RE = re.compile(r"(?<![\w#])#([A-Za-z0-9_]+)")
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
HASHTAG_NO_SPLIT_ALLOWLIST = {
    "2A",
    "4U925",
    "4U9525",
    "7NEWS",
    "7News",
    "9News",
    "9news",
    "A320",
    "ABCNews24",
    "AC360",
    "AH5017",
    "Airbus320",
    "AirbusA320",
    "Flightradar24",
    "GE235",
    "MH17",
    "MH370",
    "NMOS14",
    "November4th",
    "QZ8501",
    "abc730",
    "justice4all",
    "nyc4stl",
    "p2",
    "r4today",
}


def _normalize_emoji(text: str) -> str:
    return emoji.demojize(text, language="en", delimiters=(":", ":"))


def _normalize_mention(match: re.Match[str]) -> str:
    username = match.group(1)
    return match.group(0) if username.lower() in SOURCE_MENTION_ALLOWLIST else "@USER"


def _split_hashtag_words(value: str) -> str:
    value = value.replace("_", " ")
    value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)
    value = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", value)
    value = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", value)
    value = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", value)
    return SPACE_RE.sub(" ", value).strip()


def _normalize_hashtag(match: re.Match[str]) -> str:
    value = match.group(1)
    return value if value in HASHTAG_NO_SPLIT_ALLOWLIST else _split_hashtag_words(value)


def normalize_text(text: str, emoji_normalization: bool = True) -> str:
    text = html.unescape(str(text))
    text = RT_RE.sub("", text)
    text = URL_RE.sub("HTTPURL", text)
    text = USER_RE.sub(_normalize_mention, text)
    text = HASHTAG_RE.sub(_normalize_hashtag, text)
    if emoji_normalization:
        text = _normalize_emoji(text)
        text = EMOJI_TOKEN_RE.sub(lambda match: f" {match.group(1).replace('_', ' ')} ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def make_text_view(text: str, normalized: bool = True) -> str:
    return normalize_text(text) if normalized else str(text).strip()
