#!/usr/bin/env bash

set -u

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
skills_root=$repo_root/skills

if [ ! -d "$skills_root" ]; then
    printf 'error: skills directory not found: %s\n' "$skills_root" >&2
    exit 1
fi

find "$skills_root" \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    ! -name '.*' \
    -exec test -f '{}/SKILL.md' ';' \
    -exec basename '{}' ';' \
    | LC_ALL=C sort
