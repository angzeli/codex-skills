"""CLI for the synthetic record parser."""

import argparse
from pathlib import Path

from records import summary_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["summary"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.command == "summary":
        print(summary_report(args.path.read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
