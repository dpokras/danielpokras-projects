#!/bin/bash
# Shrink photos before committing them — keeps the repo (and page loads) small.
# Usage:  tools/resize.sh ~/Pictures/dinners/*.jpg  images/dinners
# Uses sips, which ships with macOS. No installs.
set -euo pipefail
args=("$@"); dest="${args[${#args[@]}-1]}"; unset 'args[${#args[@]}-1]'
mkdir -p "$dest"
for f in "${args[@]}"; do
  name=$(basename "$f")
  cp "$f" "$dest/$name"
  sips --resampleHeightWidthMax 2000 "$dest/$name" >/dev/null
  sips -s format jpeg -s formatOptions 78 "$dest/$name" --out "$dest/${name%.*}.jpg" >/dev/null
  [ "${name##*.}" != "jpg" ] && rm -f "$dest/$name"
  echo "  $dest/${name%.*}.jpg  ($(du -h "$dest/${name%.*}.jpg" | cut -f1))"
done
