---
name: pdf
description: Extract text, tables, and images from PDF documents
utterances:
  - "extract text from PDF"
  - "read this PDF file"
  - "parse PDF document"
  - "get tables from PDF"
  - "convert PDF to text"
keywords:
  - pdf
  - document
  - extract
  - tables
  - text extraction
---

# PDF Processing Skill

Extract and process content from PDF documents.

## Capabilities

- Text extraction with layout preservation
- Table detection and extraction
- Image extraction
- Metadata parsing
- OCR for scanned documents

## Usage

When processing PDFs:

1. **Text Extraction**: Use `pdfplumber` or `PyMuPDF` for accurate text
2. **Tables**: Use `camelot` or `tabula-py` for structured tables
3. **Images**: Extract embedded images with `PyMuPDF`
4. **OCR**: Fall back to `pytesseract` for scanned documents

## Example Commands

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

## Best Practices

- Always check if PDF is text-based or scanned
- Preserve table structure when extracting
- Handle multi-column layouts appropriately
- Extract metadata (author, date, title) when relevant
