---
name: docx
description: Process Microsoft Word documents - extract text, tables, and formatting
utterances:
  - "read Word document"
  - "extract text from docx"
  - "parse Word file"
  - "get content from .docx"
  - "process Microsoft Word"
keywords:
  - word
  - docx
  - document
  - microsoft
  - office
---

# Word Document Processing Skill

Process Microsoft Word (.docx) documents.

## Capabilities

- Text extraction with formatting
- Table extraction
- Image extraction
- Style and heading detection
- Track changes and comments

## Usage

```python
from docx import Document

doc = Document("file.docx")

# Extract paragraphs
for para in doc.paragraphs:
    print(para.text)

# Extract tables
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

## Dependencies

- `python-docx` for document parsing
- `mammoth` for HTML conversion

## Best Practices

- Preserve heading hierarchy
- Maintain list structure
- Extract embedded images when needed
- Handle tracked changes appropriately
