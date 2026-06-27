$root = "backend/app/modules/ai_smeta_ru"
$subpackages = @(
    'common',
    'document_understanding',
    'quantity_normalization',
    'completeness_checker',
    'designer_questions',
    'assumption_engine',
    'standards_mapping',
    'pre_expertise_self_check',
    'grandsmeta_excel_export',
    'estimator_package'
)

function Write-FileContent {
    param(
        [string]$Path,
        [string]$Content
    )
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Set-Content -Path $Path -Value $Content -Encoding UTF8
}

$files = @{
    "$root/__init__.py" = @'
"""AI-Smeta-RU module skeleton.

This package contains the MVP skeleton for AI-assisted Russian estimating.
"""

__all__ = [
    'common',
    'document_understanding',
    'quantity_normalization',
    'completeness_checker',
    'designer_questions',
    'assumption_engine',
    'standards_mapping',
    'pre_expertise_self_check',
    'grandsmeta_excel_export',
    'estimator_package',
]
'@

    "$root/README.md" = @'
# AI-Smeta-RU Module

## Purpose

The `ai_smeta_ru` module is a skeleton package for an AI-assisted Russian estimating MVP inside OpenConstructionERP. It is intended to support source ingestion, extraction, normalization, completeness checks, designer questions, estimator assumptions, Russian norm candidate suggestions, GrandSmeta-ready export, and package assembly.

## MVP Boundaries

- Supports draft estimate creation and review workflows only.
- Does not create final approved estimates.
- Does not connect database migrations or production-ready persistence.
- Does not implement full Russian norm or government expertise automation.
- Does not implement complex business logic yet.

## Existing OpenConstructionERP Modules Reused

The MVP skeleton is designed to reuse the following existing modules:

- `documents`
- `takeoff`
- `dwg_takeoff`
- `ai_estimator`
- `boq`
- `costs`
- `russia_pack`
- `supplier_catalogs`
- `grandsmeta_export`

## Workflow

1. source files
2. data extraction
3. structuring
4. completeness check
5. designer questions
6. estimator assumptions
7. Russian norm candidates
8. GrandSmeta-ready Excel
9. Estimator Package

## MVP Limitations

This MVP does not create final approved estimates. It is scoped to draft generation, review support, and handoff preparation for GrandSmeta.
'@

    "$root/common/__init__.py" = @'
from .base_models import *
from .enums import *
from .provenance import *
from .constants import *

__all__ = [
    'Base',
    'TimestampMixin',
    'SourceMixin',
    'ReviewMixin',
    'SourceArtifact',
    'ExtractedObject',
    'QuantityItem',
    'WorkItem',
    'MaterialItem',
    'EquipmentItem',
    'NormCandidate',
    'MissingDataIssue',
    'DesignerQuestion',
    'EstimatorAssumption',
    'PreExpertiseIssue',
    'GrandSmetaExportRow',
    'EstimatorPackage',
    'ReviewStatus',
    'SourceType',
    'NormFamily',
    'ProvenanceRecord',
    'MVP_MODULE_NAME',
    'DEFAULT_CONFIDENCE',
]
'@

    "$root/common/enums.py" = @'
from enum import Enum

class ReviewStatus(str, Enum):
    draft = 'draft'
    review_pending = 'review_pending'
    approved = 'approved'
    rejected = 'rejected'

class SourceType(str, Enum):
    pdf = 'pdf'
    scanned_pdf = 'scanned_pdf'
    docx = 'docx'
    xlsx = 'xlsx'
    dwg = 'dwg'
    dxf = 'dxf'

class NormFamily(str, Enum):
    gesn = 'GESN'
    fer = 'FER'
    ter = 'TER'
    fsnb = 'FSNB'
'@

    "$root/common/constants.py" = @'
MVP_MODULE_NAME = 'ai_smeta_ru'
DEFAULT_CONFIDENCE = 0.0
'@

    "$root/common/provenance.py" = @'
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProvenanceRecord(BaseModel):
    source_id: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    extracted_at: datetime
    notes: Optional[str] = None
'@

    "$root/common/base_models.py" = @'
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
from .enums import ReviewStatus, SourceType, NormFamily

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SourceMixin:
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    source_type = Column(SAEnum(SourceType), nullable=True)

class ReviewMixin:
    confidence = Column(Float, default=0.0)
    review_status = Column(SAEnum(ReviewStatus), default=ReviewStatus.draft)

class SourceArtifact(Base, TimestampMixin):
    __tablename__ = 'ai_smeta_source_artifact'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    original_filename = Column(String(512), nullable=False)
    source_type = Column(SAEnum(SourceType), nullable=False)
    discipline = Column(String(64), nullable=True)
    checksum = Column(String(128), nullable=True)
    metadata = Column(Text, nullable=True)
    provenance = Column(Text, nullable=True)

class ExtractedObject(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_extracted_object'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    object_type = Column(String(128), nullable=False)
    raw_text = Column(Text, nullable=True)
    normalized_text = Column(Text, nullable=True)

class QuantityItem(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_quantity_item'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    quantity = Column(Float, nullable=True)
    unit = Column(String(64), nullable=True)
    measurement_basis = Column(Text, nullable=True)

class WorkItem(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_work_item'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    discipline = Column(String(64), nullable=True)
    description = Column(Text, nullable=False)
    unit = Column(String(64), nullable=True)
    status = Column(String(64), nullable=True)
    estimated_category = Column(String(128), nullable=True)

class MaterialItem(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_material_item'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    material_name = Column(String(256), nullable=False)
    unit = Column(String(64), nullable=True)
    quantity_reference = Column(String(255), nullable=True)

class EquipmentItem(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_equipment_item'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    equipment_name = Column(String(256), nullable=False)
    quantity_reference = Column(String(255), nullable=True)
    unit = Column(String(64), nullable=True)

class NormCandidate(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_norm_candidate'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    norm_family = Column(SAEnum(NormFamily), nullable=True)
    norm_code = Column(String(128), nullable=True)
    source_basis = Column(Text, nullable=True)

class MissingDataIssue(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_missing_data_issue'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    issue_type = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=True)

class DesignerQuestion(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_designer_question'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    question_text = Column(Text, nullable=False)
    target_role = Column(String(128), nullable=True)
    priority = Column(String(32), nullable=True)

class EstimatorAssumption(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_estimator_assumption'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    assumption_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=True)

class PreExpertiseIssue(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_pre_expertise_issue'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    issue_type = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)

class GrandSmetaExportRow(Base, TimestampMixin):
    __tablename__ = 'ai_smeta_grandsmeta_export_row'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    source_reference = Column(String(255), nullable=True)
    work_item_id = Column(Integer, nullable=True)
    row_data = Column(Text, nullable=True)

class EstimatorPackage(Base, TimestampMixin, ReviewMixin):
    __tablename__ = 'ai_smeta_estimator_package'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    package_reference = Column(String(256), nullable=False)
    contents = Column(Text, nullable=True)
'@
}

foreach ($pkg in $subpackages) {
    $pkgName = $pkg -replace '_', '' | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }
    $files["$root/$pkg/__init__.py"] = "@'
\"\"\"$($pkg -replace '_',' ' | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }) subpackage.\"\"\"\n'@"
    $files["$root/$pkg/models.py"] = @"'
from dataclasses import dataclass
from typing import Optional

@dataclass
class $pkgName