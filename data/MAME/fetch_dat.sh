#!/usr/bin/env bash
# Download the latest MAME DAT pack from progetto-SNAPS and extract it.
# Requires 7z (p7zip-full) or similar.

set -euo pipefail

DEST="data/MAME"
mkdir -p "$DEST"

URL="https://www.progettosnaps.net/download/?tipo=dat_mame&file=/dats/MAME/packs/MAME_Dats_289.7z"
ARCHIVE="/tmp/MAME_Dats_289.7z"

echo "Downloading MAME 0.289 DAT pack..."
curl -L -o "$ARCHIVE" "$URL"

echo "Extracting..."
if command -v 7z >/dev/null 2>&1; then
  7z x "$ARCHIVE" -o"$DEST" -y
elif command -v 7za >/dev/null 2>&1; then
  7za x "$ARCHIVE" -o"$DEST" -y
else
  echo "7z not found. Please install p7zip-full and re-run, or extract $ARCHIVE manually."
  exit 1
fi

echo "Done. DAT files are in $DEST"
ls -lh "$DEST"
