from __future__ import annotations

import argparse
import json

from src.pipeline import build_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--text", required=True)
    parser.add_argument("--no-explain", action="store_true")
    args = parser.parse_args()

    pipeline = build_pipeline(args.config, with_explainer=not args.no_explain)
    result = pipeline.predict(args.text, explain=not args.no_explain)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

