"""Acceptance check for the synthetic docs-only fixture."""

from pathlib import Path


text = Path("README.md").read_text(encoding="utf-8")
assert "## Installation" in text, "requested heading is not corrected"
assert "Instalation" not in text, "original typo remains"
assert (
    "This deliberately awkward paragraph is unrelated to the task and must stay "
    "exactly as written even though it could be more polished perhaps."
) in text, "unrelated paragraph changed"
