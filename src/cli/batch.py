from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.config import load_config
from src.core.batch import run_batch_prediction
from src.models.registry import create_classifier


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--max-detail-rows", type=int, default=10000)
    args = parser.parse_args()

    config = load_config(args.config)
    classifier = create_classifier(config)
    classifier.load()
    content = Path(args.csv).read_text(encoding="utf-8")
    result = run_batch_prediction(classifier, content, max_detail_rows=args.max_detail_rows, config=config)
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
