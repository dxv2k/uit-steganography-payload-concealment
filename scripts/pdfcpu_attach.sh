#!/bin/bash
# pdfcpu_attach.sh: Attach a payload to a PDF using the official pdfcpu Docker image
# Usage: ./scripts/pdfcpu_attach.sh pdfs/base.pdf payloads/shell.elf pdfs/attack.pdf

set -e
set -o pipefail
set -x  # Enable bash debug mode for verbose output

if [ "$#" -ne 3 ]; then
    echo "[ERROR] Usage: $0 <base.pdf> <payload> <output.pdf>" >&2
    exit 1
fi

BASE_PDF="$1"
PAYLOAD="$2"
OUTPUT_PDF="$3"

# Print key variables
echo "[DEBUG] BASE_PDF: $BASE_PDF"
echo "[DEBUG] PAYLOAD: $PAYLOAD"
echo "[DEBUG] OUTPUT_PDF: $OUTPUT_PDF"
echo "[DEBUG] Working directory: $(pwd)"

# Ensure files exist
if [ ! -f "$BASE_PDF" ]; then
    echo "[ERROR] Base PDF not found: $BASE_PDF" >&2
    exit 2
fi
if [ ! -f "$PAYLOAD" ]; then
    echo "[ERROR] Payload file not found: $PAYLOAD" >&2
    exit 3
fi

# # Ensure output file exists (workaround for some pdfcpu versions)
# if [ ! -f "$OUTPUT_PDF" ]; then
#     echo "[INFO] Creating blank output PDF: $OUTPUT_PDF"
#     python -c "from pypdf import PdfWriter; PdfWriter().write('$OUTPUT_PDF')"
# fi

# Ensure output directory exists
OUTPUT_DIR=$(dirname "$OUTPUT_PDF")
mkdir -p "$OUTPUT_DIR"

# Construct clean paths for inside the container
CONTAINER_OUTPUT_PDF="/workspace/${OUTPUT_PDF#./}"
CONTAINER_BASE_PDF="/workspace/${BASE_PDF#./}"
CONTAINER_PAYLOAD="/workspace/${PAYLOAD#./}"

# Print the full docker command
DOCKER_CMD="docker run --rm -v '$(pwd)':/workspace pdfcpu-bin attachments add -o '$CONTAINER_OUTPUT_PDF' '$CONTAINER_BASE_PDF' '$CONTAINER_PAYLOAD'"
echo "[DEBUG] Running: $DOCKER_CMD"

# Actually run the command
docker run --rm -v "$(pwd)":/workspace pdfcpu-bin attachments add -o "$CONTAINER_OUTPUT_PDF" "$CONTAINER_BASE_PDF" "$CONTAINER_PAYLOAD"

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Payload attached: $OUTPUT_PDF"
else
    echo "[ERROR] Failed to attach payload" >&2
    exit 4
fi 