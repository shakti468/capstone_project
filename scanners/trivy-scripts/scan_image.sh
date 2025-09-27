#!/usr/bin/env bash
set -euo pipefail

IMAGE=${1:-}
OUTDIR=${2:-./scans}

if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image> [outdir]"
  exit 1
fi

mkdir -p "$OUTDIR"
OUTFILE="$OUTDIR/$(echo $IMAGE | tr '/:' '_').json"

echo "Scanning $IMAGE -> $OUTFILE"
trivy image --quiet --format json --output "$OUTFILE" "$IMAGE"
echo "done"
