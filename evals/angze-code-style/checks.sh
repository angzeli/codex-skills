#!/usr/bin/env bash

set -u

eval_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
failures=0

run_required() {
    label=$1
    shift
    printf 'CHECK %s\n' "$label"
    if "$@"; then
        printf 'PASS  %s\n' "$label"
    else
        printf 'FAIL  %s\n' "$label" >&2
        failures=$((failures + 1))
    fi
}

run_required "Python numerical behavior" \
    python3 -m unittest discover -s "$eval_root/fixtures/python" -p 'test_*.py'
run_required "Notebook contract validator" \
    python3 -B -m unittest discover -s "$eval_root/fixtures/notebook" -p 'test_*.py'
run_required "HTML and CSS fixture integrity" \
    python3 "$eval_root/fixtures/html/validate_html.py" "$eval_root/fixtures/html/index.html" "$eval_root/fixtures/html/styles.css"
run_required "Shell syntax" \
    bash -n "$eval_root/fixtures/shell/run_campaign.sh"
run_required "Adversarial protections" \
    python3 -m unittest discover -s "$eval_root/fixtures/adversarial" -p 'test_*.py'
run_required "Cross-language Shell contracts" \
    python3 "$eval_root/fixtures/contracts/test_shell_fixtures.py"
if command -v pdflatex >/dev/null 2>&1; then
    run_required "Cross-language LaTeX contracts" \
        python3 "$eval_root/fixtures/contracts/test_latex_fixtures.py"
else
    run_required "Cross-language LaTeX static contracts" \
        python3 "$eval_root/fixtures/contracts/test_latex_fixtures.py" static
fi
run_required "Cross-language HTML contracts" \
    python3 "$eval_root/fixtures/contracts/test_html_fixtures.py"

if command -v shellcheck >/dev/null 2>&1; then
    # SC2086 is the deliberate unquoted-variable challenge in the baseline fixture.
    run_required "ShellCheck (excluding deliberate SC2086)" \
        shellcheck -e SC2086 "$eval_root/fixtures/shell/run_campaign.sh"
else
    printf 'SKIP  ShellCheck is not available\n'
fi

if command -v pdflatex >/dev/null 2>&1; then
    tex_output=$(mktemp -d "${TMPDIR:-/tmp}/angze-code-style-tex.XXXXXX")
    run_required "LaTeX compilation" \
        pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$tex_output" "$eval_root/fixtures/latex/report.tex"
else
    printf 'SKIP  pdflatex is not available\n'
fi

if [ "$failures" -ne 0 ]; then
    printf '%s fixture check(s) failed\n' "$failures" >&2
    exit 1
fi

printf 'All required fixture checks passed\n'
