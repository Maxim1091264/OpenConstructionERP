from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple
import re

from app.modules.ai_smeta_ru.adapters.pdf_adapter import PdfAdapter


@dataclass
class PageClassification:
    page_number: int
    page_type: str
    discipline_guess: Optional[str]
    is_estimate_relevant: bool
    reason: str
    extracted_text_preview: str
    confidence: float


class DocumentIntelligenceRUService:
    """Prototype page classifier for Russian project documentation PDFs.

    Uses simple rule-based heuristics to assign a page type and a discipline
    guess. This is intentionally simple and designed as a prototype layer
    before any WorkItem extraction occurs.
    """

    def __init__(self) -> None:
        self.pdf = PdfAdapter()

    def classify(self, file_path: str) -> List[PageClassification]:
        pages = self.pdf.extract_pages(file_path)
        results: List[PageClassification] = []

        for page_number, text in pages:
            text = text or ""
            preview = text.strip()[:400]
            page_type, confidence, reason = self._classify_text(text)
            discipline = self._guess_discipline(text)
            is_relevant = page_type in (
                "specification",
                "bill_of_quantities",
                "drawing_sheet",
                "equipment_schedule",
                "material_schedule",
                "room_schedule",
                "cable_journal",
            )

            results.append(
                PageClassification(
                    page_number=page_number,
                    page_type=page_type,
                    discipline_guess=discipline,
                    is_estimate_relevant=is_relevant,
                    reason=reason,
                    extracted_text_preview=preview,
                    confidence=confidence,
                )
            )

        return results

    def _classify_text(self, text: str) -> Tuple[str, float, str]:
        t = (text or "").lower()
        # Short page -> likely cover
        if len(t.strip()) < 40:
            return "cover_page", 0.6, "very short page"

        # Table of contents
        if any(k in t for k in ("содержание", "оглавление")):
            return "contents", 0.92, "contains contents keyword"

        # Normative references
        if re.search(r"нормативн|нормативные|нормативные ссылки", t):
            return "normative_references", 0.9, "contains normative keywords"

        # Specification pages
        if re.search(r"спецификац|технические требования|спецификация", t):
            return "specification", 0.9, "contains specification keywords"

        # Bill of quantities / estimation tables
        if re.search(r"ведомость объемов|смета|объем работ|бюджет|итого", t):
            return "bill_of_quantities", 0.9, "contains BOQ keywords"

        # Cable journal
        if re.search(r"журнал кабелей|кабельный журнал", t):
            return "cable_journal", 0.9, "contains cable journal keywords"

        # Equipment/material schedules
        if re.search(r"ведомост.*оборудован|ведомост.*оборудов", t):
            return "equipment_schedule", 0.9, "contains equipment schedule keywords"

        if re.search(r"ведомост.*материалов|материалов", t):
            return "material_schedule", 0.88, "contains material schedule keywords"

        # Room schedule / explication
        if re.search(r"план помещений|экспликация помещений|экспликация", t):
            return "room_schedule", 0.88, "contains room schedule keywords"

        # Drawing sheet detection
        if re.search(r"лист чертежа|чертеж|drawing", t):
            return "drawing_sheet", 0.8, "likely drawing sheet"

        # General notes
        if re.search(r"примечани|общие указания|общие сведения|примечание", t):
            return "general_notes", 0.78, "general notes clues"

        # Title page heuristics: short header near top
        first_lines = "\n".join(text.splitlines()[:6])
        if len(first_lines.strip()) < 160 and sum(1 for c in first_lines if c.isupper()) > 6:
            return "title_page", 0.75, "short title-like header"

        return "irrelevant_or_unknown", 0.5, "no matching heuristics"

    def _guess_discipline(self, text: str) -> Optional[str]:
        t = (text or "").lower()
        if any(k in t for k in ("электр", "свет", "кабель", "щит", "освещ")):
            return "electrical"
        if any(k in t for k in ("канализац", "водоснабж", "водопровод", "труб")):
            return "plumbing"
        if any(k in t for k in ("конструкц", "бетон", "железобетон", "арм", "монолит")):
            return "structural"
        if any(k in t for k in ("отоплен", "вентил", "вентиляц", "кондиц")):
            return "hvac"
        return None
