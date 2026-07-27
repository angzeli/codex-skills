#!/usr/bin/env bash

set -u

usage() {
    printf 'usage: %s [skill-name]\n' "${0##*/}" >&2
}

if [ "$#" -gt 1 ]; then
    usage
    exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
evals_root=$repo_root/evals

if [ "$#" -eq 1 ]; then
    skill_name=$1
    case "$skill_name" in
        ''|*[!a-z0-9-]*|-*|*-|*--*)
            printf 'error: skill name must use lowercase kebab-case\n' >&2
            exit 2
            ;;
    esac
    if [ ! -d "$evals_root/$skill_name" ]; then
        printf 'error: evaluation directory not found: evals/%s\n' "$skill_name" >&2
        exit 1
    fi
    eval_names=$skill_name
else
    eval_names=$(find "$evals_root" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -exec basename '{}' ';' | LC_ALL=C sort)
fi

if [ -z "$eval_names" ]; then
    printf 'error: no evaluation directories found\n' >&2
    exit 1
fi

failures=0
for eval_name in $eval_names; do
    check_script=$evals_root/$eval_name/checks.sh
    if [ ! -f "$check_script" ]; then
        printf 'SKIP  %s has no checks.sh\n' "$eval_name"
        continue
    fi

    printf 'RUN   %s\n' "$eval_name"
    if bash "$check_script"; then
        printf 'PASS  %s\n' "$eval_name"
    else
        printf 'FAIL  %s\n' "$eval_name" >&2
        failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    printf 'error: %s evaluation suite(s) failed\n' "$failures" >&2
    exit 1
fi

printf 'All available fixture checks passed\n'
