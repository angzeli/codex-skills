#!/usr/bin/env bash

set -u

eval_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${ANGZE_PLOT_STYLE_PYTHON:-python3}

if ! command -v "$python_bin" >/dev/null 2>&1; then
    printf 'error: Python interpreter not found: %s\n' "$python_bin" >&2
    exit 1
fi

if ! "$python_bin" -c 'import matplotlib' >/dev/null 2>&1; then
    printf 'error: Matplotlib is unavailable in %s\n' "$python_bin" >&2
    printf 'set ANGZE_PLOT_STYLE_PYTHON to an interpreter with Matplotlib\n' >&2
    exit 1
fi

mpl_config=$(mktemp -d "${TMPDIR:-/tmp}/angze-plot-style-mpl.XXXXXX") || exit 1
trap 'rm -rf "$mpl_config"' EXIT HUP INT TERM

MPLBACKEND=Agg \
MPLCONFIGDIR="$mpl_config" \
XDG_CACHE_HOME="$mpl_config" \
PYTHONDONTWRITEBYTECODE=1 \
    "$python_bin" -m unittest discover \
    -s "$eval_root/fixtures" \
    -p 'test_*.py'
