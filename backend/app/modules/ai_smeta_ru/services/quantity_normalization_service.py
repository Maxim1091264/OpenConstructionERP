"""Service for converting extracted content into draft work and quantity items."""

from __future__ import annotations

import re
from typing import Iterable
from uuid import uuid4

from app.modules.ai_smeta_ru.domain.models import ExtractedObject, QuantityItem, WorkItem

QUANTITY_PATTERN = re.compile(
    r"(?P<quantity>\d+(?:[\.,]\d+)?)(?:\s*[-x×]?\s*)(?P<unit>[A-Za-zА-Яа-яЁё0-9/%]+)"
)


class QuantityNormalizationService:
    """Normalizes extracted text into draft estimate work items and quantities."""

    def normalize(
        self, extracted_objects: Iterable[ExtractedObject]
    ) -> tuple[list[WorkItem], list[QuantityItem]]:
        work_items: list[WorkItem] = []
        quantities: list[QuantityItem] = []

        for extracted_object in extracted_objects:
            raw_text = extracted_object.normalized_text or extracted_object.raw_text or ""
            description = raw_text.strip() or "unspecified work item"
            quantity, unit = self._parse_quantity(raw_text)

            work_item_id = str(uuid4())
            work_item = WorkItem(
                work_item_id=work_item_id,
                description=description,
                unit=unit,
                source_reference=extracted_object.object_id,
            )
            work_items.append(work_item)

            quantities.append(
                QuantityItem(
                    quantity_id=str(uuid4()),
                    work_item_id=work_item_id,
                    quantity=quantity,
                    unit=unit,
                    measurement_basis=raw_text,
                    source_reference=extracted_object.object_id,
                )
            )

        return work_items, quantities

    def _parse_quantity(self, text: str) -> tuple[float | None, str | None]:
        if not text:
            return None, None

        match = QUANTITY_PATTERN.search(text)
        if match:
            raw_value = match.group("quantity").replace(",", ".")
            try:
                quantity = float(raw_value)
            except ValueError:
                quantity = None
            unit = match.group("unit").strip()
            return quantity, unit

        tokens = [token.strip() for token in text.split() if token.strip()]
        if len(tokens) >= 2:
            try:
                quantity = float(tokens[-2].replace(",", "."))
                unit = tokens[-1]
                return quantity, unit
            except ValueError:
                pass

        return None, None
