# django-ocr

A lightweight Django-based OCR package that extracts text from images and allows dynamic mapping of extracted text into structured dictionaries.

## Features
- Extracts text from images using Tesseract OCR
- Supports dynamic key-value mapping for structured text output
- Simple API for easy integration into Django projects
- Fully customizable mapping to extract expected information

## Installation
You can install `django-ocr` using pip:

```bash
pip install django-ocr
```

## Dependencies
Make sure you have `Tesseract-OCR` installed on your system. If not, install it using:

- **Ubuntu/Debian:**
  ```bash
  sudo apt install tesseract-ocr
  ```
- **MacOS:**
  ```bash
  brew install tesseract
  ```
- **Windows:**
  Download and install from [Tesseract's official site](https://github.com/tesseract-ocr/tesseract).

## Usage

### 1. Extract Text from an Image

```python
from django_ocr import process_image

text = process_image("sample_image.png")
print(text)  # Output: Extracted text from the image
```

### 2. Extract and Map Text to Structured Dictionary

If you have an image containing structured information, such as:
```
Name: John
Last Name: Doe
```
You can map it dynamically:

```python
from django_ocr import process_image_with_mapping

image_path = "sample_image.png"
mappings = {
    "first_name": ["Name"],
    "last_name": ["Last Name"]
}

result = process_image_with_mapping(image_path, mappings)
print(result)
# Output: {'first_name': 'John', 'last_name': 'Doe'}
```

## API Reference

### `process_image(image_path: str) -> str`
Extracts text from an image and returns it as a string.

### `process_image_with_mapping(image_path: str, mappings: dict) -> dict`
Extracts text from an image and maps values to a structured dictionary based on provided mappings.

- `image_path`: Path to the image file
- `mappings`: A dictionary where keys represent desired output fields, and values are lists of keywords to search for

## Customization
You can define your own mappings dynamically based on the expected text format.

Example for extracting an ID and an email:
```python
mappings = {
    "user_id": ["ID", "User ID"],
    "email": ["Email"]
}
```

## Contributing
Feel free to open issues or submit pull requests to improve this package!

## License
MIT License

