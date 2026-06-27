# TASK 004 — First AI-Smeta-RU Extraction Prototype

## 1. Goal

Implement a local prototype for the first AI-Smeta-RU extraction pipeline. The prototype should ingest XLSX, DOCX, and PDF input files, extract structured text and tables, normalize draft work items and quantities, and export an estimator review Excel package.

This prototype is intentionally constrained:
- no database migrations
- no production persistence
- no Russian norm matching
- no GrandSmeta final import
- only local prototype services and tests

## 2. Scope

The implementation includes:

- domain models for source artifacts, extracted objects, work items, and quantity items
- adapters for XLSX, DOCX, and PDF file extraction
- a document understanding service to dispatch by file type
- a quantity normalization service to turn extracted objects into draft review entities
- an estimator review Excel export with `WorkItems`, `QuantityItems`, and `ProcessingLog` sheets
- a CLI demo script to run extraction, normalization, and export

## 3. Prototype Boundaries

This task does not implement:
- persistence or database models
- production-quality AI matching or norm lookup
- GrandSmeta import workflows
- reviewer workflows beyond a simple Excel export

## 4. Usage

Run the prototype demo script from the repository root:

```bash
python scripts/demo_ai_smeta_extraction.py path/to/sample.xlsx
```

An output workbook named `sample-review.xlsx` will be generated alongside the input file by default.

## 5. Notes

- `openpyxl` is used for XLSX export and import.
- `python-docx` is required for DOCX extraction.
- `pypdf` or `PyMuPDF` is required for PDF extraction.
- Missing dependencies fail gracefully with a clear message.
