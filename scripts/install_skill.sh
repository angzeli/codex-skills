#!/usr/bin/env bash

set -u

usage() {
    printf 'usage: %s [--dry-run] <skill-name>\n' "${0##*/}" >&2
}

dry_run=false
skill_name=
for argument in "$@"; do
    case "$argument" in
        --dry-run)
            dry_run=true
            ;;
        -* )
            usage
            exit 2
            ;;
        *)
            if [ -n "$skill_name" ]; then
                usage
                exit 2
            fi
            skill_name=$argument
            ;;
    esac
done

if [ -z "$skill_name" ]; then
    usage
    exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
source_path=$repo_root/skills/$skill_name
install_root=${CODEX_SKILLS_INSTALL_ROOT:-"$HOME/.agents/skills"}
destination=$install_root/$skill_name

"$script_dir/check_skill.sh" "$skill_name" || exit 1

printf 'Source:      %s\n' "$source_path"
printf 'Destination: %s\n' "$destination"

if [ -L "$destination" ] && [ -d "$destination" ]; then
    resolved_source=$(CDPATH= cd -- "$source_path" && pwd -P)
    resolved_destination=$(CDPATH= cd -- "$destination" && pwd -P)
    if [ "$resolved_source" = "$resolved_destination" ]; then
        printf 'Already installed with the correct symbolic link\n'
        exit 0
    fi
fi

if [ "$dry_run" = true ]; then
    if [ -e "$destination" ] || [ -L "$destination" ]; then
        printf 'DRY RUN: preserve the existing installation as a timestamped backup\n'
    else
        printf 'DRY RUN: create the installation directory if needed\n'
    fi
    printf 'DRY RUN: link the individual skill directory\n'
    exit 0
fi

if [ -e "$install_root" ] && [ ! -d "$install_root" ]; then
    printf 'error: installation root exists but is not a directory: %s\n' "$install_root" >&2
    exit 1
fi
mkdir -p "$install_root"

backup_path=
if [ -e "$destination" ] || [ -L "$destination" ]; then
    timestamp=$(date '+%Y%m%d-%H%M%S')
    backup_path=$destination.backup-$timestamp
    suffix=0
    while [ -e "$backup_path" ] || [ -L "$backup_path" ]; do
        suffix=$((suffix + 1))
        backup_path=$destination.backup-$timestamp-$suffix
    done
    mv "$destination" "$backup_path"
    printf 'Preserved existing installation: %s\n' "$backup_path"
fi

if ! ln -s "$source_path" "$destination"; then
    printf 'error: failed to create symbolic link: %s\n' "$destination" >&2
    if [ -n "$backup_path" ] && [ ! -e "$destination" ] && [ ! -L "$destination" ]; then
        mv "$backup_path" "$destination"
        printf 'Restored previous installation after link failure\n' >&2
    fi
    exit 1
fi

printf 'Installed %s\n' "$skill_name"
