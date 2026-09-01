# Synthetic record parser

Implement a bounded `summary` report through the existing parser and CLI.

Input rows have `label,value`. The report format is exactly:

```text
records=<count> total=<sum with two decimal places>
```

Ignore blank lines. Reject malformed rows. Keep `normalize_label_awkwardly` unchanged; it represents an unrelated cleanup opportunity.
