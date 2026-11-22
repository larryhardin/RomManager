#!/usr/bin/env bash
# Download the latest MAME DAT pack from progetto-SNAPS and extract it.
# Note: The upstream file is a .7z archive. gunzip only handles .gz.
# This script currently expects a .gz; you may need to convert or use 7z.

set -euo pipefail

DEST="data/MAME"
mkdir -p "$DEST"

URL="https://www.progettosnaps.net/download/?tipo=dat_mame&file=/dats/MAME/packs/MAME_Dats_289.7z"
ARCHIVE="/tmp/MAME_Dats_289.7z"

echo "Downloading MAME 0.289 DAT pack..."
curl -L -o "$ARCHIVE" "$URL"

echo "Note: Downloaded file is .7z. gunzip cannot extract it."
echo "If you have a .gz version, rename/adjust the URL and use:"
echo "  gunzip -c /tmp/file.gz > destination"

# Placeholder for gunzip (will fail on .7z)
if [[ "$ARCHIVE" == *.gz ]]; then
  gunzip -c "$ARCHIVE" > "$DEST/mame.dat"
  echo "Extracted with gunzip."
else
  echo "File is not .gz. Please extract the .7z manually or install p7zip-full."
  echo "Archive left at: $ARCHIVE"
  exit 1
fi

echo "Done. DAT files are in $DEST"
ls -lh "$DEST"
