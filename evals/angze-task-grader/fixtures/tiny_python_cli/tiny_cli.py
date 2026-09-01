"""Tiny synthetic greeting CLI."""

import argparse


def render_greetings(name: str, count: int | None) -> list[str]:
    """Return the requested number of greeting lines."""
    resolved_count = count or 1
    return [f"hello {name}"] * resolved_count


def legacy_banner(text: str) -> str:
    """Deliberately awkward unrelated helper."""
    return "*** " + text + " ***"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args(argv)
    for line in render_greetings(args.name, args.count):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
