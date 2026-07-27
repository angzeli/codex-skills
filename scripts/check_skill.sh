#!/usr/bin/env bash

set -u

usage() {
    printf 'usage: %s <skill-name>\n' "${0##*/}" >&2
}

fail() {
    printf 'error: %s\n' "$1" >&2
    exit 1
}

if [ "$#" -ne 1 ]; then
    usage
    exit 2
fi

skill_name=$1
case "$skill_name" in
    ''|*[!a-z0-9-]*|-*|*-|*--*)
        fail "skill name must use lowercase kebab-case"
        ;;
esac

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
skill_root=$repo_root/skills/$skill_name
skill_file=$skill_root/SKILL.md

if [ ! -f "$skill_file" ]; then
    fail "missing skills/$skill_name/SKILL.md"
fi

first_line=$(sed -n '1p' "$skill_file")
if [ "$first_line" != '---' ]; then
    fail "skills/$skill_name/SKILL.md must begin with a YAML frontmatter delimiter"
fi

closing_line=$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "$skill_file")
if [ -z "$closing_line" ]; then
    fail "skills/$skill_name/SKILL.md has no closing frontmatter delimiter"
fi

frontmatter=$(sed -n "2,$((closing_line - 1))p" "$skill_file")
if ! printf '%s\n' "$frontmatter" | awk '
    /^[[:space:]]*$/ || /^[[:space:]]*#/ { next }
    /^[A-Za-z0-9_-]+:[[:space:]]*[^[:space:]].*$/ { next }
    { exit 1 }
'; then
    fail "skills/$skill_name/SKILL.md contains malformed or unsupported frontmatter"
fi

name_count=$(printf '%s\n' "$frontmatter" | grep -c '^name:[[:space:]]*' || true)
description_count=$(printf '%s\n' "$frontmatter" | grep -c '^description:[[:space:]]*' || true)
if [ "$name_count" -ne 1 ]; then
    fail "frontmatter must contain exactly one name field"
fi
if [ "$description_count" -ne 1 ]; then
    fail "frontmatter must contain exactly one description field"
fi

declared_name=$(printf '%s\n' "$frontmatter" | sed -n 's/^name:[[:space:]]*//p')
case "$declared_name" in
    \"*\") declared_name=${declared_name#\"}; declared_name=${declared_name%\"} ;;
    \'*\') declared_name=${declared_name#\'}; declared_name=${declared_name%\'} ;;
esac
if [ "$declared_name" != "$skill_name" ]; then
    fail "frontmatter name '$declared_name' does not match directory '$skill_name'"
fi

description=$(printf '%s\n' "$frontmatter" | sed -n 's/^description:[[:space:]]*//p')
case "$description" in
    \"*\") description=${description#\"}; description=${description%\"} ;;
    \'*\') description=${description#\'}; description=${description%\'} ;;
esac
if [ "${#description}" -lt 40 ]; then
    fail "frontmatter description must be meaningful (at least 40 characters)"
fi
case "$description" in
    *TODO*|*TBD*|*placeholder*) fail "frontmatter description still contains placeholder text" ;;
esac

personal_matches=$(find "$skill_root" -type f -exec grep -IHnE '(/Users/[^/$[:space:]]+/|/home/[^/$[:space:]]+/|[A-Za-z]:\\Users\\[^\\]+\\)' {} + 2>/dev/null || true)
if [ -n "$personal_matches" ]; then
    printf '%s\n' "$personal_matches" >&2
    fail "runtime files contain a personal absolute path"
fi

while IFS= read -r -d '' symlink_path; do
    if [ ! -e "$symlink_path" ]; then
        fail "broken symbolic link in runtime skill: ${symlink_path#"$repo_root/"}"
    fi
done < <(find "$skill_root" -type l -print0)

while IFS= read -r -d '' markdown_file; do
    while IFS= read -r link_match; do
        reference=${link_match#](}
        reference=${reference%)}
        reference=${reference#<}
        reference=${reference%>}
        reference=${reference%%#*}
        reference=${reference%%\?*}
        case "$reference" in
            ''|'#'*|http://*|https://*|mailto:*|skill://*|'$'*) continue ;;
        esac
        if [ ! -e "$(dirname -- "$markdown_file")/$reference" ]; then
            fail "broken relative reference '$reference' in ${markdown_file#"$repo_root/"}"
        fi
    done < <(grep -Eo '\]\([^)]+\)' "$markdown_file" || true)
done < <(find "$skill_root" -type f -name '*.md' -print0)

printf 'PASS %s\n' "$skill_name"
