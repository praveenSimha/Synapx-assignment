from pathlib import Path
from typing import Union
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    pdf_path = Path(pdf_path)
    reader = PdfReader(pdf_path)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)
