from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND.resolve()))

from app.modules.ai_smeta_ru.services.document_intelligence_ru_service import DocumentIntelligenceRUService
from app.modules.ai_smeta_ru.export.page_classification_excel_export import PageClassificationExcelExport


def main() -> int:
    parser = argparse.ArgumentParser(description="PDF page classification demo for AI-Smeta-RU")
    parser.add_argument("file", help="Path to PDF file to classify")
    parser.add_argument("--output", help="Output Excel path (optional)", default=None)
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}-page-classification.xlsx")

    svc = DocumentIntelligenceRUService()
    try:
        pages = svc.classify(str(input_path))
        print(f"Classified {len(pages)} pages")

        exporter = PageClassificationExcelExport()
        exporter.export(pages, str(output_path))
        print(f"Wrote page classification workbook: {output_path}")
    except Exception as exc:
        print(f"Classification failed: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
