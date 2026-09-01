"""Small synthetic record parser."""


def parse_records(text: str) -> list[tuple[str, float]]:
    records = []
    for line in text.splitlines():
        if not line.strip():
            continue
        label, raw_value = line.split(",", maxsplit=1)
        records.append((label, float(raw_value)))
    return records


def summary_report(text: str) -> str:
    """Return the documented bounded report."""
    return "TODO"


def normalize_label_awkwardly(label: str) -> str:
    """Deliberately awkward unrelated helper."""
    return ((label.strip()).strip()).lower()
