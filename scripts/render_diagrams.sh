#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for source in assets/diagrams/*.svg; do
  inkscape "$source" --export-type=png --export-filename="${source%.svg}.png" --export-width=2000 >/dev/null 2>&1
  inkscape "$source" --export-type=png --export-filename="${source%.svg}-preview.png" --export-width=1000 >/dev/null 2>&1
done
