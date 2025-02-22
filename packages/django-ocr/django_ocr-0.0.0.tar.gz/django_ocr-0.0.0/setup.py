from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-ocr",
    version="0.0.0",
    author="fereshteh",
    author_email="fereshtehahmadi01@gmail.com",
    description="A lightweight Django-based OCR package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fereshtehAhmadi/django-ocr",
    packages=find_packages(),
    install_requires=[
        "django",
        "pytesseract",
        "Pillow",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
