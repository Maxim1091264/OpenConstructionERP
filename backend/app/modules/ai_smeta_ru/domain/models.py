from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class SourceArtifact:
    """Represents an ingested source file for review and drafting."""
    artifact_id: str
    original_filename: str
    source_type: str
    discipline: Optional[str] = None
    checksum: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExtractedObject:
    """Represents a structured extraction from a source artifact."""
    object_id: str
    artifact_id: str
    object_type: str
    raw_text: Optional[str] = None
    normalized_text: Optional[str] = None
    confidence: float = 0.0


@dataclass(slots=True)
class QuantityItem:
    """Represents a quantity or measurement candidate."""
    quantity_id: str
    work_item_id: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    measurement_basis: Optional[str] = None


@dataclass(slots=True)
class WorkItem:
    """Represents a candidate draft estimate work item."""
    work_item_id: str
    description: str
    discipline: Optional[str] = None
    unit: Optional[str] = None
    status: str = "draft"
    estimated_category: Optional[str] = None


@dataclass(slots=True)
class MaterialItem:
    """Represents a material reference for a work item."""
    material_id: str
    work_item_id: Optional[str] = None
    material_name: Optional[str] = None
    unit: Optional[str] = None
    quantity_reference: Optional[str] = None


@dataclass(slots=True)
class EquipmentItem:
    """Represents equipment referenced by a work item."""
    equipment_id: str
    work_item_id: Optional[str] = None
    equipment_name: Optional[str] = None
    unit: Optional[str] = None
    quantity_reference: Optional[str] = None


@dataclass(slots=True)
class NormCandidate:
    """Represents a candidate Russian norm mapping suggestion."""
    candidate_id: str
    work_item_id: Optional[str] = None
    norm_family: Optional[str] = None
    norm_code: Optional[str] = None
    confidence: float = 0.0
    source_basis: Optional[str] = None


@dataclass(slots=True)
class MissingDataIssue:
    """Represents missing or ambiguous information blocking a clean draft."""
    issue_id: str
    work_item_id: Optional[str] = None
    issue_type: str = "missing_data"
    description: str = ""
    severity: str = "medium"


@dataclass(slots=True)
class DesignerQuestion:
    """Represents a follow-up question for designers or engineers."""
    question_id: str
    work_item_id: Optional[str] = None
    question_text: str = ""
    target_role: Optional[str] = None
    priority: str = "medium"


@dataclass(slots=True)
class EstimatorAssumption:
    """Represents an explicit assumption used in drafting."""
    assumption_id: str
    work_item_id: Optional[str] = None
    assumption_text: str = ""
    rationale: Optional[str] = None


@dataclass(slots=True)
class PreExpertiseIssue:
    """Represents a self-check issue that may block expertise readiness."""
    issue_id: str
    work_item_id: Optional[str] = None
    issue_type: str = "pre_expertise"
    description: str = ""
    recommendation: Optional[str] = None


@dataclass(slots=True)
class GrandSmetaExportRow:
    """Represents a row candidate for GrandSmeta-ready export."""
    row_id: str
    work_item_id: Optional[str] = None
    row_data: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EstimatorPackage:
    """Represents the full review package prepared for estimator handoff."""
    package_id: str
    package_name: str
    grand_smeta_import_excel: Optional[str] = None
    estimator_review_excel: Optional[str] = None
    designer_questions: list[DesignerQuestion] = field(default_factory=list)
    estimator_assumptions: list[EstimatorAssumption] = field(default_factory=list)
    norm_candidates: list[NormCandidate] = field(default_factory=list)
    missing_data_report: list[MissingDataIssue] = field(default_factory=list)
    pre_expertise_report: list[PreExpertiseIssue] = field(default_factory=list)
    processing_protocol: Optional[str] = None
