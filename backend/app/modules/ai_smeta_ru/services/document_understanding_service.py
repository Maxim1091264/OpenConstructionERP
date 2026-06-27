"""Service orchestrating document format adapters for prototype extraction."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from app.modules.ai_smeta_ru.adapters.docx_adapter import DocxAdapter
from app.modules.ai_smeta_ru.adapters.pdf_adapter import PdfAdapter
from app.modules.ai_smeta_ru.adapters.xlsx_adapter import XlsxAdapter
from app.modules.ai_smeta_ru.domain.models import ExtractedObject, SourceArtifact

SUPPORTED_FORMATS = {
    "xlsx": XlsxAdapter,
    "xls": XlsxAdapter,
    "docx": DocxAdapter,
    "pdf": PdfAdapter,
}


class DocumentUnderstandingService:
    """Routes an input file to the correct adapter for extraction."""

    def extract(self, file_path: str, source_type: str | None = None) -> list[ExtractedObject]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file does not exist: {file_path}")

        ext = (source_type or Path(file_path).suffix.lstrip(".")).lower()
        if not ext:
            raise ValueError("Unable to determine source type for document understanding")

        adapter_cls = SUPPORTED_FORMATS.get(ext)
        if adapter_cls is None:
            raise ValueError(f"Unsupported source type: {ext}")

        artifact = SourceArtifact(
            artifact_id=str(uuid4()),
            original_filename=Path(file_path).name,
            source_type=ext,
            storage_path=str(Path(file_path).resolve()),
        )
        adapter = adapter_cls()
        return adapter.extract(file_path=file_path, artifact_id=artifact.artifact_id)
