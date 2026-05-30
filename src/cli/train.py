from __future__ import annotations

import argparse

from src.config import ensure_output_dirs, load_config
from src.training import train


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_output_dirs(config)
    checkpoint = train(config)
    print(f"saved checkpoint: {checkpoint}")


if __name__ == "__main__":
    main()

