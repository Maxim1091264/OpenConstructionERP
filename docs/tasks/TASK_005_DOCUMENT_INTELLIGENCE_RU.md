# TASK 005 — Document Intelligence (RU) Page Classification

## Problem found in the first prototype

The initial AI-Smeta-RU prototype treated whole PDF pages as `WorkItem`s, which
caused many false positives: pages that contain a variety of unrelated content
were incorrectly ingested as single work items. This produced noisy drafts and
poor downstream quantity extraction quality.

## Goal of this task

Introduce a lightweight page classification layer that determines which pages
are estimate-relevant and which are not. Only after identifying estimate-
relevant pages will the extraction pipeline attempt to extract tables,
specifications, and work-item candidates.

This is a prototype (no persistence, no AI model integration yet) and uses
rule-based heuristics tailored for Russian project documentation.

## New pipeline stage

1. Ingest PDF file.
2. Run page-level text extraction.
3. Classify each page into one of the page types (cover, title, contents,
   specification, bill_of_quantities, drawing_sheet, etc.).
4. Mark pages that are likely estimate-relevant (specifications, BOQ,
   schedules, drawings) for downstream extraction.
5. Export a human-readable page-classification workbook for estimator review.

## Why WorkItem extraction must wait for page classification

- Pages can contain mixed content: header/footer, table of contents, notes,
  drawings and tables in the same page. Extracting WorkItems before
  classification leads to extracting irrelevant or fragmented items.
- Limiting extraction to estimate-relevant pages reduces noise, improves
  precision for quantity parsing, and keeps the human-in-the-loop review
  manageable.

## New prototype components

- `backend/app/modules/ai_smeta_ru/services/document_intelligence_ru_service.py`
  — rule-based page classifier returning `PageClassification` objects.
- `backend/app/modules/ai_smeta_ru/adapters/pdf_adapter.py` — updated to
  provide page-by-page text extraction API.
- `backend/app/modules/ai_smeta_ru/export/page_classification_excel_export.py`
  — writes classification results to an Excel workbook.
- `scripts/demo_ai_smeta_pdf_page_classification.py` — demo script that accepts
  a PDF path and writes `<source>-page-classification.xlsx`.

## Next planned step

Implement targeted extraction that runs only on pages flagged as
`is_estimate_relevant`. That step will:

- Extract tables and structured rows from classified pages.
- Create `ExtractedObject` entries per table/paragraph instead of per page.
- Run quantity normalization on the filtered extracted objects.
