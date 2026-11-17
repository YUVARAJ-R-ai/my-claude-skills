#!/usr/bin/env bash
# render-model.sh: Compile an OpenSCAD model to STL and optionally generate a PNG preview.
# Usage: ./render-model.sh <input.scad> [output.stl] [--image]

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input.scad> [output.stl] [--image]"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_STL="${2:-${INPUT_FILE%.scad}.stl}"
GENERATE_IMAGE=false

for arg in "$@"; do
    if [ "$arg" == "--image" ] || [ "$arg" == "-i" ]; then
        GENERATE_IMAGE=true
    fi
done

if ! command -v openscad >/dev/null 2>&1; then
    echo "Error: openscad is not found in PATH." >&2
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found." >&2
    exit 1
fi

echo "==> Rendering 3D model to STL: $OUTPUT_STL"
openscad -o "$OUTPUT_STL" "$INPUT_FILE"

if [ -f "$OUTPUT_STL" ]; then
    SIZE=$(du -h "$OUTPUT_STL" | cut -f1)
    echo "✔ STL successfully generated: $OUTPUT_STL ($SIZE)"
else
    echo "✘ Failed to generate STL." >&2
    exit 1
fi

if [ "$GENERATE_IMAGE" = true ]; then
    IMAGE_OUT="${OUTPUT_STL%.stl}.png"
    echo "==> Rendering preview image: $IMAGE_OUT"
    openscad --render --imgsize 1024,768 --colorscheme "Tomorrow Night" -o "$IMAGE_OUT" "$INPUT_FILE"
    echo "✔ Preview image generated: $IMAGE_OUT"
fi
