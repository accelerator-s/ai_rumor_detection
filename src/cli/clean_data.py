from __future__ import annotations

import argparse
import json

from src.config import ensure_output_dirs, load_config, resolve_path
from src.data.dataset import export_cleaned_datasets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_output_dirs(config)
    report = export_cleaned_datasets(config)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"saved cleaned train: {resolve_path(config['paths']['cleaned_train_csv'])}")
    print(f"saved cleaned val: {resolve_path(config['paths']['cleaned_val_csv'])}")
    print(f"saved cleaning report: {resolve_path(config['paths']['cleaning_report_json'])}")


if __name__ == "__main__":
    main()
