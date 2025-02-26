from .latecript_app import LatecriptApp, LatecriptSettings
import json
from pathlib import Path

import argparse


def load_settings(settings_path: Path) -> dict | None:
    if not settings_path.exists():
        return None
    with settings_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch Latecript")
    parser.add_argument(
        "--settings_file",
        help="Path to alternative settings JSON file",
        type=str,
        default=None,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = None
    if args.settings_file:
        settings = load_settings(Path(args.settings_file))

    LatecriptApp(
        settings=LatecriptSettings.model_validate(settings)
        if settings is not None
        else None
    ).run()


if __name__ == "__main__":
    main()
