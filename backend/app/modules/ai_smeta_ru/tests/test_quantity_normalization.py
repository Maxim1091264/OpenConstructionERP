from __future__ import annotations

from app.modules.ai_smeta_ru.domain.models import ExtractedObject
from app.modules.ai_smeta_ru.services.quantity_normalization_service import QuantityNormalizationService


def test_quantity_normalization_parses_simple_row() -> None:
    extracted = ExtractedObject(
        object_id="test-1",
        artifact_id="artifact-1",
        object_type="table_row",
        raw_text="Concrete slab 12.5 m3",
        normalized_text="Concrete slab 12.5 m3",
        confidence=0.95,
    )
    normalizer = QuantityNormalizationService()

    work_items, quantity_items = normalizer.normalize([extracted])

    assert len(work_items) == 1
    assert len(quantity_items) == 1
    assert work_items[0].description == "Concrete slab 12.5 m3"
    assert work_items[0].unit == "m3"
    assert quantity_items[0].quantity == 12.5
    assert quantity_items[0].unit == "m3"
    assert quantity_items[0].source_reference == "test-1"
