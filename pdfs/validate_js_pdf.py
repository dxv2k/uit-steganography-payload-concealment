import logging
import traceback
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, FilePath
from pypdf import PdfReader

# Set up logging
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "validate_js_pdf.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def extract_js_code(js_obj) -> Optional[str]:
    """Try to extract JavaScript code from a PDF object."""
    try:
        if hasattr(js_obj, 'get') and js_obj.get("/JS"):
            return str(js_obj.get("/JS"))
        if hasattr(js_obj, 'get') and js_obj.get("/JavaScript"):
            return str(js_obj.get("/JavaScript"))
        return str(js_obj)
    except Exception as e:
        logging.warning(f"Could not extract JS code: {e}")
        return None

def list_attachments(reader: PdfReader):
    attachments = []
    try:
        catalog = reader.trailer["/Root"]
        if "/Names" in catalog and "/EmbeddedFiles" in catalog["/Names"]:
            ef_dict = catalog["/Names"]["/EmbeddedFiles"]
            if "/Names" in ef_dict:
                ef_names = ef_dict["/Names"]
                for i in range(0, len(ef_names), 2):
                    name = ef_names[i]
                    file_spec = ef_names[i+1]
                    attachments.append((name, file_spec))
    except Exception as e:
        logging.warning(f"Could not list attachments: {e}")
    return attachments

def log_catalog(reader: PdfReader, label: str):
    try:
        catalog = reader.trailer["/Root"]
        logging.info(f"[{label}] Catalog: {catalog}")
        print(f"[{label}] Catalog: {catalog}")
        if "/Names" in catalog:
            logging.info(f"[{label}] /Names: {catalog['/Names']}")
            print(f"[{label}] /Names: {catalog['/Names']}")
            if "/EmbeddedFiles" in catalog["/Names"]:
                logging.info(f"[{label}] /EmbeddedFiles: {catalog['/Names']['/EmbeddedFiles']}")
                print(f"[{label}] /EmbeddedFiles: {catalog['/Names']['/EmbeddedFiles']}")
            if "/JavaScript" in catalog["/Names"]:
                logging.info(f"[{label}] /JavaScript: {catalog['/Names']['/JavaScript']}")
                print(f"[{label}] /JavaScript: {catalog['/Names']['/JavaScript']}")
        if "/OpenAction" in catalog:
            logging.info(f"[{label}] /OpenAction: {catalog['/OpenAction']}")
            print(f"[{label}] /OpenAction: {catalog['/OpenAction']}")
    except Exception as e:
        logging.warning(f"Could not log catalog for {label}: {e}")
        print(f"Could not log catalog for {label}: {e}")

class PDFValidationInput(BaseModel):
    pdf_path: FilePath


def validate_pdf_js(pdf_path: FilePath) -> bool:
    """
    Validates that the PDF is not corrupted and contains JavaScript actions.
    Args:
        pdf_path (FilePath): Path to the PDF file.
    Returns:
        bool: True if PDF is valid and contains JavaScript, False otherwise.
    """
    try:
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        metadata = reader.metadata
        logging.info(f"Successfully opened PDF: {pdf_path}")
        logging.info(f"Number of pages: {num_pages}")
        logging.info(f"Metadata: {metadata}")
        print(f"PDF '{pdf_path}' opened successfully.")
        print(f"Number of pages: {num_pages}")
        print(f"Metadata: {metadata}")
        # Log and print catalog/root object
        log_catalog(reader, "VALIDATION")
        # List and print attachments
        attachments = list_attachments(reader)
        if attachments:
            print(f"Found {len(attachments)} attachment(s):")
            logging.info(f"Found {len(attachments)} attachment(s):")
            for name, file_spec in attachments:
                print(f"  - {name}: {file_spec}")
                logging.info(f"  - {name}: {file_spec}")
        else:
            print("No attachments found.")
            logging.info("No attachments found.")
        # Check for JavaScript in OpenAction or Names
        js_found = False
        js_details = ""
        catalog = reader.trailer["/Root"]
        if "/OpenAction" in catalog:
            open_action = catalog["/OpenAction"]
            js_code = extract_js_code(open_action)
            if open_action.get("/S") == "/JavaScript" or "/JavaScript" in str(open_action):
                js_found = True
                js_details += f"/OpenAction: {open_action}\n"
                if js_code:
                    js_details += f"JavaScript code: {js_code}\n"
        # Check for JavaScript in Names dictionary
        if "/Names" in catalog:
            names = catalog["/Names"]
            if "/JavaScript" in names:
                js_found = True
                js_details += f"/Names: {names}\n"
                js_code = extract_js_code(names["/JavaScript"]) if hasattr(names, 'get') and names.get("/JavaScript") else None
                if js_code:
                    js_details += f"JavaScript code in /Names: {js_code}\n"
        if js_found:
            logging.info(f"JavaScript action found in PDF: {pdf_path}")
            logging.info(f"JavaScript details: {js_details}")
            print(f"JavaScript action found in PDF!")
            print(f"Details: {js_details}")
            return True
        else:
            logging.warning(f"No JavaScript action found in PDF: {pdf_path}")
            print(f"No JavaScript action found in PDF. Checked /OpenAction and /Names.")
            return False
    except Exception as e:
        logging.error(f"Failed to validate PDF: {e}\n{traceback.format_exc()}")
        print(f"Failed to validate PDF. See log: {LOG_FILE}")
        return False


def main():
    """Test block for PDF JS validation."""
    pdf_path = OUTPUT_DIR / "attack_with_js.pdf"
    args = PDFValidationInput(pdf_path=pdf_path)
    validate_pdf_js(args.pdf_path)

if __name__ == "__main__":
    main() 