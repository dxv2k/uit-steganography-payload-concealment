# End-to-End Reverse Shell + Stego-in-PDF + JavaScript PoC: TODO

## 1. Project Initialization
- [x] Scaffold the directory structure as per project_structure.md
- [x] Add initial README.md with workflow overview
- [x] Create requirements.txt with recommended Python packages
- [x] Add .gitkeep or placeholder files in all empty directories for version control

## 2. Payload Generation (Linux)
- [x] Implement scripts/build_payload.sh to generate a Linux reverse shell payload (shell.elf) using msfvenom or bash
- [x] Place generated payload in payloads/shell.elf

## 3. PDF Stego Embedding
- [x] Use Dockerized pdfcpu to attach shell.elf as a file attachment to base.pdf, outputting attack.pdf (see scripts/pdfcpu_attach.sh)
- [x] Place base.pdf in pdfs/ (created with pypdf for validity)
- [x] Verify attachment in attack.pdf using pdfcpu or pypdf

## 4. JavaScript Injection (PDF)
- [ ] Implement pdfs/js_injector.py to inject JavaScript into attack.pdf (e.g., alert or attempt to export attachment)
- [ ] Output final attack.pdf with JS

## 5. Simulation Script (Victim Side)
- [ ] Implement scripts/simulate_execution.sh to extract the payload from attack.pdf and execute it (mimicking JS extraction)

## 6. Listener Setup
- [ ] Implement scripts/run_listener.sh to start a netcat or msfconsole listener on the attacker's machine
- [ ] Add msfvenom/msfconsole usage example for reverse shell listener

## 7. Dockerized Environment
- [x] Implement docker/attacker.Dockerfile and docker/target.Dockerfile for attacker and victim nodes (Linux)
- [x] Implement docker/pdfcpu.Dockerfile for pdfcpu CLI
- [x] Implement docker/compose.yml to orchestrate both containers and networking

## 8. Output & Logging
- [x] Ensure all scripts log actions and errors to output/ directory (and/or verbose output)
- [x] Store all generated artifacts (attack.pdf, logs, extracted payloads) in output/

## 9. Testing & Documentation
- [x] Add __main__ test blocks to all Python scripts (where applicable)
- [x] Add usage examples and workflow steps to README.md
- [x] Document each step for reproducibility

---

## Notes
- Focus on Linux for initial PoC. Windows support can be added later.
- For PoC, manual extraction of the payload from PDF is acceptable.
- Use simple, well-documented tools and scripts for clarity and reproducibility.
- Scripts now include verbose/debug output for easier troubleshooting. 