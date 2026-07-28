#!/usr/bin/env bash
# Publish a deterministic subset of processed kinetic results.

if [[ $# -ne 2 ]]; then
    echo "usage: $0 SOURCE_DIR PUBLISH_DIR" >&2
    exit 64
fi

source_dir=$1
publish_dir=$2
scale=${PUBLISH_SCALE:-1e-9}

if [[ ! -d "$source_dir" ]]; then
    echo "missing source directory: $source_dir" >&2
    exit 66
fi

mkdir -p "$publish_dir"
manifest="$publish_dir/manifest.tsv"
temporary="$publish_dir/.manifest.$$"

printf "file\trows\tsha256\n" > "$temporary"

find "$source_dir" -maxdepth 1 -type f -name "*.csv" -print |
    LC_ALL=C sort |
    while IFS= read -r source_file
    do
        filename=$(basename "$source_file")
        destination="$publish_dir/$filename"

        # Convert the delay column from nanoseconds to seconds.
        awk -F, -v OFS=, -v factor="$scale" '
            NR == 1 { print; next }
            NF >= 2 { $1 = sprintf("%.12g", $1 * factor) }
            { print }
        ' "$source_file" > "$destination"

        rows=$(awk 'END { print NR - 1 }' "$destination")
        checksum=$(shasum -a 256 "$destination" | awk '{print $1}')
        printf "%s\t%s\t%s\n" "$filename" "$rows" "$checksum"
    done >> "$temporary"

mv "$temporary" "$manifest"