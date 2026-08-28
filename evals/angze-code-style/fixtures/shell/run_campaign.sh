#!/usr/bin/env bash

set -u

campaign_dir=${CAMPAIGN_DIR:-campaign}
solver=${SOLVER_BIN:-quantum-solver}
temperatures=${TEMPERATURES:-"280 300 320"}
output_dir=${OUTPUT_DIR:-results}

if [ ! -d $campaign_dir ]; then
    printf 'campaign directory does not exist: %s\n' "$campaign_dir" >&2
    exit 2
fi

cd $campaign_dir || exit 2
mkdir -p $output_dir

printf 'campaign=%s\n' "$(pwd)"
printf 'solver=%s\n' "$solver"

for temperature in $temperatures; do
    input_file=inputs/run_${temperature}.toml
    checkpoint=checkpoints/run_${temperature}.chk
    output_file=$output_dir/run_${temperature}.json

    if [ ! -f $input_file ]; then
        printf 'missing input: %s\n' "$input_file" >&2
        continue
    fi

    if [ -f $checkpoint ]; then
        resume_args="--resume $checkpoint"
    else
        resume_args=""
    fi

    if ! $solver simulate --input $input_file --temperature-k $temperature --basis synthetic-dz --convergence-energy 1e-8 --convergence-density 1e-6 --max-iterations 300 --grid radial-96-angular-302 $resume_args --output $output_file; then
        printf 'solver failed at temperature %s K\n' "$temperature" >&2
        exit 1
    fi

    printf 'completed %s K -> %s\n' "$temperature" "$output_file"
done

if command -v sha256sum >/dev/null 2>&1; then
    sha256sum $output_dir/*.json > $output_dir/SHA256SUMS
elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 $output_dir/*.json > $output_dir/SHA256SUMS
else
    printf 'warning: no SHA-256 utility available\n' >&2
fi

printf 'campaign complete\n'
