"""Adapter for PDF-based data extraction with page-level APIs."""

from __future__ import annotations

import re
from uuid import uuid4
from typing import List

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
    """Extracts page-level text from PDFs and provides helper APIs.

    The adapter exposes `extract_pages()` which returns a list of (page_number, text)
    and `extract()` which returns one ExtractedObject per page (not per block).
    """

    def extract_pages(self, file_path: str) -> List[tuple[int, str]]:
        """Return list of (page_number, text) for every page in the PDF.

        Uses pypdf when available, falls back to PyMuPDF (fitz).
        """
        if PdfReader is not None:
            return self._pages_with_pypdf(file_path)

        if fitz is not None:
            return self._pages_with_pymupdf(file_path)

        raise ImportError(
            "PDF page extraction requires pypdf or pymupdf. Install one of them with: pip install pypdf pymupdf"
        )

    def extract(self, file_path: str, artifact_id: str | None = None) -> list[ExtractedObject]:
        pages = self.extract_pages(file_path)
        artifact_id = artifact_id or str(uuid4())
        objects: list[ExtractedObject] = []

        for page_number, text in pages:
            object_id = f"pdf-page-{page_number}-{uuid4().hex}"
            objects.append(
                ExtractedObject(
                    object_id=object_id,
                    artifact_id=artifact_id,
                    object_type="page",
                    raw_text=text,
                    normalized_text=text,
                    confidence=0.85,
                )
            )

        return objects

    def _pages_with_pypdf(self, file_path: str) -> List[tuple[int, str]]:
        reader = PdfReader(file_path)
        pages: List[tuple[int, str]] = []
        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append((page_index, text))
        return pages

    def _pages_with_pymupdf(self, file_path: str) -> List[tuple[int, str]]:
        doc = fitz.open(file_path)
        pages: List[tuple[int, str]] = []
        for page_index, page in enumerate(doc, start=1):
            text = page.get_text("text") or ""
            pages.append((page_index, text))
        return pages

    def _split_text_blocks(self, text: str) -> list[str]:
        blocks = [block.strip() for block in re.split(r"\n{2,}", text) if block.strip()]
        if not blocks and text.strip():
            blocks = [line.strip() for line in text.splitlines() if line.strip()]
        return blocks
