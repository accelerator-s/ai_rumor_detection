from __future__ import annotations

import argparse
import json

from src.core.llm import load_explain_llm_settings
from src.pipeline import build_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--text", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--no-explain", action="store_true")
    args = parser.parse_args()

    explain = not args.no_explain
    pipeline = build_pipeline(args.config, with_explainer=explain)
    llm_config = load_explain_llm_settings() if explain else None
    result = pipeline.predict(args.text, event=args.event, explain=explain, llm_config=llm_config)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

