from __future__ import annotations

import argparse
import json

from src.config import ensure_output_dirs, load_config
from src.evaluation.evaluator import evaluate
from src.models.registry import create_classifier


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--split", choices=["val", "train"], default="val")
    parser.add_argument("--checkpoint", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_output_dirs(config)
    csv_path = config["paths"]["val_csv"] if args.split == "val" else config["paths"]["train_csv"]
    classifier = create_classifier(config, checkpoint=args.checkpoint)
    result = evaluate(classifier, csv_path, config["paths"]["model_dir"], config=config)
    print(json.dumps(result["overall"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

