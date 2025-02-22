import pytesseract
from PIL import Image
import re


def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def parse_text_to_dict(text, mappings):
    """
    Parse extracted text based on user defined mappings.

    mappings = {
        "first_name": "نام",
        "last_name": "نام خانوادگی",
        "birth_date": "تاریخ تولد"
    }
    """
    data = {}

    for key, keyword in mappings.items():
        pattern = rf"{keyword}[:\s]+([\w\s\d-/]+)"
        match = re.search(pattern, text)

        if match:
            data[key] = match.group(1).strip()

    return data
