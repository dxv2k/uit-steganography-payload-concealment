For your end-to-end **reverse shell + stego-in-PDF + JavaScript execution PoC**, here's a clean, modular folder structure you can use:

---

## 📁 Suggested Project Structure

```
reverse-stego-poc/
├── docker/
│   ├── attacker.Dockerfile
│   ├── target.Dockerfile
│   └── compose.yml
│
├── payloads/
│   ├── shell.elf             # Output payload (generated)
│   ├── shell.ps1             # Optional PowerShell variant
│   └── download_stub.sh      # Tiny stager that downloads the real payload
│
├── pdfs/
│   ├── base.pdf              # Clean carrier PDF
│   ├── stego_embedder.py     # Script to hide payload in PDF
│   ├── js_injector.py        # Inject JS into PDF to extract payload
│   └── attack.pdf            # Final malicious PDF
│
├── scripts/
│   ├── build_payload.sh      # msfvenom-based ELF builder
│   ├── run_listener.sh       # Metasploit or netcat listener
│   └── simulate_execution.sh # Target-side extractor + runner (for Docker)
│
├── server/
│   └── http_server.py        # Simple HTTP file server (Python FastAPI)
│
├── output/
│   └── [generated files]     # Artifacts (attack.pdf, logs, sessions)
│
├── .env                      # Config: LHOST, LPORT, etc.
├── README.md
└── requirements.txt          # (Optional) Python packages for stego/pdf tools
```

---

## 📦 Folder Role Breakdown

| Folder       | Purpose                                                                 |
|--------------|-------------------------------------------------------------------------|
| `docker/`    | Dockerfiles and `compose.yml` for attacker, target, optional web server |
| `payloads/`  | All stagers, reverse shells, polyglot binaries, etc.                    |
| `pdfs/`      | Original PDF, scripts to embed payload + JS, final PDF                  |
| `scripts/`   | Build pipeline helpers, PoC simulation scripts                          |
| `server/`    | Local HTTP server to host payload if using 2-stage delivery             |
| `output/`    | Generated payloads, PDFs, logs, extracted shellcode, etc.               |

---

## 🧪 Workflow Summary

1. **Build payload**  
   → `scripts/build_payload.sh` writes `shell.elf` → `payloads/`

2. **Embed in PDF**  
   → `pdfs/stego_embedder.py` takes `base.pdf` and `shell.elf`, outputs to `attack.pdf`

3. **Inject JS**  
   → `pdfs/js_injector.py` embeds JS to extract/run payload inside `attack.pdf`

4. **Run simulation**  
   → `scripts/simulate_execution.sh` mimics PDF-JS behavior (in Docker target)

5. **Serve (optional)**  
   → `server/http_server.py` serves payloads over HTTP for the 2-stage case

6. **Spin up env**  
   → `docker/compose.yml` sets up attacker, target, and listener nodes

---

## 🛠 Recommended Python Tools (for `requirements.txt`)

```txt
pypdf
pdfcpu
click
requests
flask            # optional, for hosting
```

---
