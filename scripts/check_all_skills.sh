#!/usr/bin/env bash

set -u

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skills=$("$script_dir/list_skills.sh") || exit 1

if [ -z "$skills" ]; then
    printf 'error: no valid skill directories found\n' >&2
    exit 1
fi

failures=0
for skill_name in $skills; do
    if ! "$script_dir/check_skill.sh" "$skill_name"; then
        failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    printf 'error: %s skill validation(s) failed\n' "$failures" >&2
    exit 1
fi

printf 'All %s skill(s) passed validation\n' "$(printf '%s\n' "$skills" | wc -l | tr -d ' ')"
