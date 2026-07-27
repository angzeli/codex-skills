#!/usr/bin/env bash

set -u

usage() {
    printf 'usage: %s [--dry-run]\n' "${0##*/}" >&2
}

dry_run=false
if [ "$#" -gt 1 ]; then
    usage
    exit 2
fi
if [ "$#" -eq 1 ]; then
    if [ "$1" != '--dry-run' ]; then
        usage
        exit 2
    fi
    dry_run=true
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skills=$("$script_dir/list_skills.sh") || exit 1

if [ -z "$skills" ]; then
    printf 'error: no valid skill directories found\n' >&2
    exit 1
fi

failures=0
for skill_name in $skills; do
    printf 'INSTALL %s\n' "$skill_name"
    if [ "$dry_run" = true ]; then
        if "$script_dir/install_skill.sh" --dry-run "$skill_name"; then
            printf 'PASS    %s\n' "$skill_name"
        else
            printf 'FAIL    %s\n' "$skill_name" >&2
            failures=$((failures + 1))
        fi
    elif "$script_dir/install_skill.sh" "$skill_name"; then
        printf 'PASS    %s\n' "$skill_name"
    else
        printf 'FAIL    %s\n' "$skill_name" >&2
        failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    printf 'error: %s skill installation(s) failed\n' "$failures" >&2
    exit 1
fi

printf 'All skill installations completed successfully\n'
