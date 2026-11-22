#!/usr/bin/env bash
# Download clrmamepro into this folder.
# Note: official site may require browsing; adjust URL if needed.

set -euo pipefail

DEST="data/MAME/Tools/clrmamepro"
mkdir -p "$DEST"

echo "Official download page: https://mamedev.emulab.it/clrmamepro/"
echo "Please download the latest 64-bit zip from the site and extract it here."
echo "Example (if direct link is available):"
echo "  curl -L -o /tmp/clrmamepro.zip <URL>"
echo "  unzip /tmp/clrmamepro.zip -d $DEST"

echo "Folder ready at $DEST"
