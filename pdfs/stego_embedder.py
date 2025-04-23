# NOTE: not using 
# NOTE: not using 
# NOTE: not using 
# NOTE: not using 

import sys
import os
import traceback
import logging
from typing import Optional
from pypdf import PdfReader, PdfWriter

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class EmbedderInput:
    base_pdf: str
    payload_file: str
    output_pdf: str

    def __init__(self, base_pdf: str, payload_file: str, output_pdf: str):
        self.base_pdf = base_pdf
        self.payload_file = payload_file
        self.output_pdf = output_pdf

class EmbedderOutput:
    success: bool
    message: str
    output_pdf: Optional[str]

    def __init__(self, success: bool, message: str, output_pdf: Optional[str] = None):
        self.success = success
        self.message = message
        self.output_pdf = output_pdf

def attach_payload_to_pdf(input_data: EmbedderInput) -> EmbedderOutput:
    """
    Attach a file to a PDF as an embedded file attachment.
    """
    try:
        if not os.path.isfile(input_data.base_pdf):
            msg = f"Base PDF not found: {input_data.base_pdf}"
            logging.error(msg)
            return EmbedderOutput(False, msg)
        if not os.path.isfile(input_data.payload_file):
            msg = f"Payload file not found: {input_data.payload_file}"
            logging.error(msg)
            return EmbedderOutput(False, msg)

        reader = PdfReader(input_data.base_pdf)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(input_data.payload_file, "rb") as f:
            payload_data = f.read()
            writer.add_attachment(os.path.basename(input_data.payload_file), payload_data)

        with open(input_data.output_pdf, "wb") as out_f:
            writer.write(out_f)

        msg = f"Successfully attached {input_data.payload_file} to {input_data.base_pdf} -> {input_data.output_pdf}"
        logging.info(msg)
        return EmbedderOutput(True, msg, input_data.output_pdf)
    except Exception as e:
        tb = traceback.format_exc()
        logging.error(f"Exception during PDF embedding: {e}\n{tb}")
        return EmbedderOutput(False, f"Exception: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Attach a payload to a PDF as a file attachment.")
    parser.add_argument('--base', type=str, default="pdfs/base.pdf", help="Path to base PDF")
    parser.add_argument('--payload', type=str, default="payloads/shell.elf", help="Path to payload file")
    parser.add_argument('--output', type=str, default="pdfs/attack.pdf", help="Path to output PDF")
    args = parser.parse_args()

    input_data = EmbedderInput(args.base, args.payload, args.output)
    result = attach_payload_to_pdf(input_data)
    if result.success:
        print(f"[SUCCESS] {result.message}")
    else:
        print(f"[FAIL] {result.message}") 