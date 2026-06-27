from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
BACKEND = ROOT / ".." / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND.resolve()))

from app.modules.ai_smeta_ru.adapters.docx_adapter import DocxAdapter
from app.modules.ai_smeta_ru.adapters.pdf_adapter import PdfAdapter
from app.modules.ai_smeta_ru.adapters.xlsx_adapter import XlsxAdapter
from app.modules.ai_smeta_ru.export.estimator_review_excel_export import EstimatorReviewExcelExport
from app.modules.ai_smeta_ru.services.document_understanding_service import DocumentUnderstandingService
from app.modules.ai_smeta_ru.services.quantity_normalization_service import QuantityNormalizationService


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run AI-Smeta-RU prototype extraction and export a review workbook"
    )
    parser.add_argument("file", help="Path to the sample XLSX, DOCX, or PDF file")
    parser.add_argument(
        "--output",
        help="Path to write the review Excel workbook. Defaults to <input>-review.xlsx",
        default=None,
    )
    args = parser.parse_args()
    input_path = Path(args.file).resolve()

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}-review.xlsx")
    if output_path.exists():
        print(f"Overwriting existing output file: {output_path}")

    try:
        service = DocumentUnderstandingService()
        extracted_objects = service.extract(str(input_path))
        print(f"Extracted {len(extracted_objects)} objects from {input_path.name}")

        normalizer = QuantityNormalizationService()
        work_items, quantity_items = normalizer.normalize(extracted_objects)
        print(f"Generated {len(work_items)} work items and {len(quantity_items)} quantity items")

        exporter = EstimatorReviewExcelExport()
        exporter.export(work_items=work_items, quantity_items=quantity_items, output_path=str(output_path))
        print(f"Review workbook written to: {output_path}")

    except Exception as exc:
        print(f"Extraction failed: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
