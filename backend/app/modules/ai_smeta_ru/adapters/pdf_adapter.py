"""Adapter for PDF-based data extraction from text-friendly PDFs."""

from __future__ import annotations

import re
from uuid import uuid4

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None  # type: ignore[assignment]

try:
    import fitz
except ImportError:  # pragma: no cover
    fitz = None  # type: ignore[assignment]

from app.modules.ai_smeta_ru.domain.models import ExtractedObject


class PdfAdapter:
    """Extracts text blocks from PDF files using available PDF text readers."""

    def extract(self, file_path: str, artifact_id: str | None = None) -> list[ExtractedObject]:
        if PdfReader is not None:
            return self._extract_with_pypdf(file_path, artifact_id)

        if fitz is not None:
            return self._extract_with_pymupdf(file_path, artifact_id)

        raise ImportError(
            "PDF extraction requires pypdf or pymupdf. Install one of them with: pip install pypdf pymupdf"
        )

    def _extract_with_pypdf(self, file_path: str, artifact_id: str | None) -> list[ExtractedObject]:
        reader = PdfReader(file_path)
        artifact_id = artifact_id or str(uuid4())
        objects: list[ExtractedObject] = []

        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for block_index, block in enumerate(self._split_text_blocks(text), start=1):
                object_id = f"pdf-pypdf-{page_index}-{block_index}-{uuid4().hex}"
                objects.append(
                    ExtractedObject(
                        object_id=object_id,
                        artifact_id=artifact_id,
                        object_type="paragraph",
                        raw_text=block,
                        normalized_text=block,
                        confidence=0.8,
                    )
                )

        return objects

    def _extract_with_pymupdf(self, file_path: str, artifact_id: str | None) -> list[ExtractedObject]:
        doc = fitz.open(file_path)
        artifact_id = artifact_id or str(uuid4())
        objects: list[ExtractedObject] = []

        for page_index, page in enumerate(doc, start=1):
            text = page.get_text("text") or ""
            for block_index, block in enumerate(self._split_text_blocks(text), start=1):
                object_id = f"pdf-pymupdf-{page_index}-{block_index}-{uuid4().hex}"
                objects.append(
                    ExtractedObject(
                        object_id=object_id,
                        artifact_id=artifact_id,
                        object_type="paragraph",
                        raw_text=block,
                        normalized_text=block,
                        confidence=0.8,
                    )
                )

        return objects

    def _split_text_blocks(self, text: str) -> list[str]:
        blocks = [block.strip() for block in re.split(r"\n{2,}", text) if block.strip()]
        if not blocks and text.strip():
            blocks = [line.strip() for line in text.splitlines() if line.strip()]
        return blocks
