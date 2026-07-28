#!/usr/bin/env bash
# Synthetic ORCA batch runner used as a readability and behaviour-preservation fixture.

if [[ $# -lt 2 || $# -gt 4 ]]; then
    echo "usage: $0 SOURCE_DIR OUTPUT_DIR [opt|sp] [PATTERN]" >&2
    exit 64
fi

src=$1
dst=$2
mode=${3:-opt}
pat=${4:-*.xyz}
orca=${ORCA_BIN:-orca}
method=${METHOD:-wB97X-D4}
basis=${BASIS:-ma-def2-TZVP}
solvent=${SOLVENT:-Water}
n=${NPROCS:-8}
mem=${MAXCORE_MB:-2000}
dry=${DRY_RUN:-0}
keep=${KEEP_TMP:-0}

if [[ ! -d "$src" ]]; then echo "missing source directory: $src" >&2; exit 66; fi
case "$mode" in opt) job="Opt TightOpt" ;; sp) job="" ;; *) echo "bad mode: $mode" >&2; exit 64 ;; esac

mkdir -p "$dst/inputs" "$dst/outputs"
tmp=$(mktemp -d "${TMPDIR:-/tmp}/orca-batch.XXXXXX") || exit 70

cleanup(){
    if [[ "$keep" != 1 && -n "$tmp" && -d "$tmp" ]]; then
        rm -rf "$tmp"
    fi
}
trap cleanup EXIT HUP INT TERM

manifest_tmp="$tmp/manifest.tsv"
files="$tmp/files.txt"
printf "name\tmode\tatoms\tstatus\tenergy_hartree\tinput_sha256\toutput_sha256\n" > "$manifest_tmp"

find "$src" -maxdepth 1 -type f -name "$pat" -print | LC_ALL=C sort > "$files"

if [[ ! -s "$files" ]]; then
    mv "$manifest_tmp" "$dst/manifest.tsv"
    echo "no matching structures" >&2
    exit 3
fi

bad=0

while IFS= read -r xyz
do
    stem=$(basename "$xyz")
    stem=${stem%.xyz}
    atoms=$(sed -n '1p' "$xyz" | tr -d '[:space:]')

    if [[ ! "$atoms" =~ ^[0-9]+$ ]]; then
        echo "invalid atom count: $xyz" >&2
        bad=$((bad+1))
        printf "%s\t%s\t-\tinvalid_xyz\t-\t-\t-\n" "$stem" "$mode" >> "$manifest_tmp"
        continue
    fi

    inp="$dst/inputs/$stem.inp"
    out="$dst/outputs/$stem.out"

    {
        printf "! %s %s TightSCF RIJCOSX NoSym SMD(%s) %s\n\n" "$method" "$basis" "$solvent" "$job"
        printf "%%pal\n  nprocs %s\nend\n\n" "$n"
        printf "%%maxcore %s\n\n" "$mem"
        printf "%%output\n  Print[P_Basis] 2\nend\n\n"
        printf "* xyzfile 0 1 %s\n" "$xyz"
    } > "$inp"

    rc=0

    if [[ "$dry" == 1 ]]; then
        energy=$(awk -v count="$atoms" 'BEGIN { printf "%.12f", -100.0 - count * 0.123456 }')
        {
            printf "Program Version 6.1.1\n"
            printf "Number of atoms                             %s\n" "$atoms"
            printf "FINAL SINGLE POINT ENERGY     %s\n" "$energy"
            printf "ORCA TERMINATED NORMALLY\n"
        } > "$out"
    else
        "$orca" "$inp" > "$out" 2>&1
        rc=$?
    fi

    status=failed
    energy=-

    if [[ -f "$out" ]] && grep -q "ORCA TERMINATED NORMALLY" "$out"; then
        status=ok
        energy=$(awk '/FINAL SINGLE POINT ENERGY/{value=$NF} END{if(value!="") print value}' "$out")
        if [[ -z "$energy" ]]; then
            status=missing_energy
            energy=-
            bad=$((bad+1))
        fi
    else
        bad=$((bad+1))
        if [[ "$rc" -eq 0 ]]; then status=abnormal_termination; else status="exit_$rc"; fi
    fi

    in_hash=$(shasum -a 256 "$inp" | awk '{print $1}')
    if [[ -f "$out" ]]; then out_hash=$(shasum -a 256 "$out" | awk '{print $1}'); else out_hash=-; fi

    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$stem" "$mode" "$atoms" "$status" "$energy" "$in_hash" "$out_hash" >> "$manifest_tmp"
done < "$files"

mv "$manifest_tmp" "$dst/manifest.tsv"

if [[ "$bad" -gt 0 ]]; then
    echo "$bad calculation(s) failed validation" >&2
    exit 2
fi

printf "processed %s structure(s)\n" "$(awk 'END { print NR - 1 }' "$dst/manifest.tsv")"