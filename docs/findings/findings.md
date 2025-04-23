# PDF Payload Extraction & Execution: Findings Report

## Overview
This report documents the technical findings, issues, and limitations encountered during the attempt to use PDF JavaScript and embedded files for payload extraction and execution (reverse shell PoC). The goal was to create a PDF that could deliver and trigger a payload (e.g., shell.elf) via embedded attachments and JavaScript, with a focus on both browser and Adobe Reader environments.

---

## 1. Approach & Workflow
- **Payload (shell.elf) embedded** in a multi-page PDF using `pdfcpu`.
- **JavaScript injected** using `pypdf` to automate extraction via `this.exportDataObject`.
- **Validation and debugging** performed with custom scripts and manual inspection in Adobe Reader and browsers.

---

## 2. Key Findings

### A. Browser Limitations
- **Browsers (Edge, Chrome, Firefox, Safari) do not support Acrobat JavaScript APIs** (e.g., `this.exportDataObject`).
- **No browser PDF viewer allows JavaScript to access or extract embedded files.**
- **No browser PDF viewer allows auto-download or execution of embedded files via PDF JavaScript.**
- **User interaction is always required for any file extraction, and even then, only if the viewer supports it.**

### B. Adobe Acrobat Reader Limitations
- **Adobe Reader supports `this.exportDataObject`, but only with user prompts.**
- **Silent extraction or execution is not possible.**
- **The attachment name in the PDF must match exactly the `cName` in the JavaScript.**
- **If the PDF structure is not 100% correct (especially the `/Names` dictionary and `/EmbeddedFiles`), extraction fails with `TypeError: Invalid argument type`.**
- **Merging `/EmbeddedFiles` and `/JavaScript` in the `/Names` dictionary is error-prone and not reliably supported by Python PDF libraries.**

### C. PDF Structure Issues
- **Copying or merging `/Names` entries (especially `/EmbeddedFiles`) using Python libraries like `pypdf` is fragile.**
- **Direct assignment of Python lists instead of `ArrayObject` causes PDF corruption.**
- **Even with correct types, the resulting PDF may not be recognized by Adobe Reader as having valid attachments.**

---

## 3. Evidence & Debugging
- **Repeated errors:** `Extraction failed: TypeError: Invalid argument type.`
- **Validator output:** Attachments present in input PDF, but missing or malformed in output after JS injection.
- **Manual inspection:** Attachments not visible in Adobe Reader after JS injection, even when present before.
- **PDF tools (`pdfcpu`, `pdf-parser`):** Confirmed attachment loss or structure corruption after manipulation.

---

## 4. Root Causes
- **PDF standard is complex and not all features are supported by libraries.**
- **PDF viewers (especially browsers) intentionally block file system access and JS extraction for security.**
- **Adobe Reader requires exact structure and naming for embedded file extraction.**
- **Python PDF libraries do not reliably merge or preserve `/Names` entries with both `/EmbeddedFiles` and `/JavaScript`.**

---

## 5. Recommendations
- **PDF is not a reliable vector for automated payload extraction or execution in modern environments.**
- **For browser-based PoC, use a web page, not a PDF.**
- **For Adobe Reader PoC, expect only user-driven extraction with prompts, and only if the PDF structure is perfect.**
- **If you must use PDF, consider using commercial tools or manual editing for precise structure, but this is not recommended for automation.**
- **Focus on user education, detection, and defense rather than offensive automation via PDF.**

---

## 6. Conclusion

- **PDF-based payload delivery and execution is highly constrained by modern security controls and technical limitations.**
- **Automated, cross-platform, or browser-based extraction is not feasible.**
- **Manual extraction with user prompts is possible in Adobe Reader, but fragile and not suitable for robust PoC automation.**
- **Alternative vectors (web, macro-enabled docs, etc.) may be more practical for PoC, but always require explicit authorization and ethical use.** 