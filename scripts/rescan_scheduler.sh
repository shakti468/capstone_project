#!/bin/bash
# Rescan all images every 24h (or on demand)

IMAGES_FILE="samples/sample-images.txt"
LOGFILE="logs/rescan.log"
mkdir -p logs

while read -r img; do
  echo "Rescanning $img..."
  python3 scripts/scan_with_exceptions.py "$img" >> "$LOGFILE" 2>&1
done < "$IMAGES_FILE"

echo "✅ Rescan complete. Reports in scans/, log in $LOGFILE"
