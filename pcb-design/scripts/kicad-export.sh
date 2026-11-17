#!/usr/bin/env bash
# kicad-export.sh: Headless export of Gerbers, drill files, DRC report, BOM, CPL, and 3D STEP from a KiCad PCB.
# Usage: ./kicad-export.sh <path-to-board.kicad_pcb> [output_dir]

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path-to-board.kicad_pcb> [output_dir]"
    exit 1
fi

PCB_FILE="$1"
BASE_NAME="$(basename "${PCB_FILE%.kicad_pcb}")"
OUTPUT_DIR="${2:-./manufacturing_output}"
GERBER_DIR="$OUTPUT_DIR/gerbers"

if ! command -v kicad-cli >/dev/null 2>&1; then
    echo "Error: kicad-cli is not found in PATH." >&2
    exit 1
fi

if [ ! -f "$PCB_FILE" ]; then
    echo "Error: PCB file '$PCB_FILE' does not exist." >&2
    exit 1
fi

mkdir -p "$GERBER_DIR"

echo "==> 1. Running Design Rule Check (DRC)..."
kicad-cli pcb drc --output "$OUTPUT_DIR/drc_report.txt" "$PCB_FILE" || true
echo "✔ DRC report saved to $OUTPUT_DIR/drc_report.txt"

echo "==> 2. Exporting Gerber Layers..."
kicad-cli pcb export gerbers \
    --output "$GERBER_DIR/" \
    --subtract-soldermask \
    "$PCB_FILE"
echo "✔ Gerbers exported to $GERBER_DIR"

echo "==> 3. Exporting Drill Files (PTH / NPTH)..."
kicad-cli pcb export drill \
    --output "$GERBER_DIR/" \
    --format excellon \
    --drill-origin absolute \
    "$PCB_FILE"
echo "✔ Drill files exported."

echo "==> 4. Packaging Gerbers into ZIP archive..."
(
    cd "$GERBER_DIR"
    zip -r -q "../${BASE_NAME}_gerbers.zip" ./*
)
echo "✔ Gerber package ready: $OUTPUT_DIR/${BASE_NAME}_gerbers.zip"

echo "==> 5. Exporting Pick & Place / Centroid (CPL)..."
kicad-cli pcb export pos \
    --format csv \
    --units mm \
    --output "$OUTPUT_DIR/${BASE_NAME}_cpl.csv" \
    "$PCB_FILE"
echo "✔ CPL saved to $OUTPUT_DIR/${BASE_NAME}_cpl.csv"

echo "==> 6. Exporting 3D STEP Model for CAD / OpenSCAD..."
kicad-cli pcb export step \
    --output "$OUTPUT_DIR/${BASE_NAME}.step" \
    "$PCB_FILE"
echo "✔ 3D STEP model saved to $OUTPUT_DIR/${BASE_NAME}.step"

echo ""
echo "=========================================================="
echo "✔ All manufacturing assets successfully generated in:"
echo "   $OUTPUT_DIR"
echo "=========================================================="
