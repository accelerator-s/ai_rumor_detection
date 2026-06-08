from __future__ import annotations

import argparse

from src.config import ensure_output_dirs, load_config
from src.training import train


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--event", default=None, help="train single event (0-6); omit to train all events")
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_output_dirs(config)

    if args.event is not None:
        checkpoint = train(config, event_id=args.event)
        print(f"saved checkpoint: {checkpoint}")
    else:
        for eid in range(7):
            print(f"\n{'='*60}")
            print(f"Training Event {eid}")
            print(f"{'='*60}")
            checkpoint = train(config, event_id=str(eid))
            print(f"Event {eid} saved: {checkpoint}")


if __name__ == "__main__":
    main()
