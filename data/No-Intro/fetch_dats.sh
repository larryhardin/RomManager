#!/usr/bin/env bash
# Fetch No-Intro DATs from the community mirror.
# Run from the repo root.

set -euo pipefail

DEST="data/No-Intro"
mkdir -p "$DEST"

echo "Cloning community mirror (shallow)..."
git clone --depth 1 https://github.com/libretro-mirrors/nointro-db.git /tmp/nointro-db || true

echo "Copying DATs..."
cp -v /tmp/nointro-db/*.dat "$DEST/" || echo "No DATs copied"

echo "Done. DATs are in $DEST"
echo "Note: Original source is https://datomatic.no-intro.org/"
