#!/bin/bash

INPUT="${1:-binary.bin}"
N="${2:-100}"
OUT="/dev/null"

if [[ ! -f "$INPUT" ]]; then
    echo "Нет файла: $INPUT" >&2
    exit 1
fi

bench() {
    local name="$1"; shift
    local start end total_ms avg_ms
    start=$(date +%s%3N)
    for ((i = 0; i < N; i++)); do
        "$@" >/dev/null 2>&1
    done
    end=$(date +%s%3N)
    total_ms=$(( end - start ))
    avg_ms=$(awk -v ns="$total_ms" -v n="$N" 'BEGIN{printf "%.2f", ns/n}')
    printf "%-18s total: %7d ms   avg: %8s ms   (%d итераций)\n" \
           "$name" "$total_ms" "$avg_ms" "$N"
}

bench "YAML (ручной)" python parser_bin_to_yaml.py     "$INPUT" "$OUT"
bench "YAML (lib yaml)" python super_parser_bin_to_yaml.py "$INPUT" "$OUT"
bench "XML  (lib ET)"     python super_parser_bin_to_xml.py      "$INPUT" "$OUT"
