#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载已训练好的模型到 models/outputs/ 目录。
"""

import os
import sys
import urllib.request

BASE_URL = "https://model.files.accelerators.site/KI4mU3jG0eX8mI1g"
FILES = [
    "config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "training_metadata.json",
    "model.safetensors",
    "tfidf_model.joblib",
]
NUM_EVENTS = 7
OUTPUT_ROOT = os.path.join("models", "outputs")

# 服务器上确实不存在的文件：event_2 没有 tfidf_model.joblib。
MISSING = {(2, "tfidf_model.joblib")}


def _progress(label, block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        ratio = min(downloaded / total_size, 1.0)
        bar = "█" * int(28 * ratio) + "░" * (28 - int(28 * ratio))
        sys.stdout.write(f"\r  {label} [{bar}] {ratio * 100:5.1f}%")
    else:
        sys.stdout.write(f"\r  {label} {downloaded / 1024 / 1024:.1f}MB")
    sys.stdout.flush()


def main():
    for i in range(NUM_EVENTS):
        for fname in FILES:
            if (i, fname) in MISSING:
                continue
            url = f"{BASE_URL}/event_{i}/{fname}"
            dest = os.path.join(OUTPUT_ROOT, f"event_{i}", fname)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            label = os.path.relpath(dest)
            urllib.request.urlretrieve(
                url, dest, reporthook=lambda b, s, t, lbl=label: _progress(lbl, b, s, t)
            )
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
