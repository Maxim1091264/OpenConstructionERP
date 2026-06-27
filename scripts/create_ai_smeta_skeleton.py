from pathlib import Path

root = Path('backend/app/modules/ai_smeta_ru')
subpackages = [
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
root.mkdir(parents=True, exist_ok=True)
for pkg in subpackages:
    (root / pkg).mkdir(parents=True, exist_ok=True)

files = {
    root / '__init__.py': '''"""AI-Smeta-RU module skeleton.

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
''',
    root / 'README.md': '''# AI-Smeta-RU Module

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
''',
    root / 'common' / '__init__.py': '''from .base_models import *
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
''',
    root / 'common' / 'enums.py': '''from enum import Enum

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
''',
    root / 'common' / 'constants.py': '''MVP_MODULE_NAME = 'ai_smeta_ru'
DEFAULT_CONFIDENCE = 0.0
''',
    root / 'common' / 'provenance.py': '''from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProvenanceRecord(BaseModel):
    source_id: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    extracted_at: datetime
    notes: Optional[str] = None
''',
    root / 'common' / 'base_models.py': '''from datetime import datetime
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
''',
}

for pkg in subpackages:
    pkg_name = pkg.title().replace('_', '')
    files[root / pkg / '__init__.py'] = f'"""{pkg.replace("_", " ").title()} subpackage."""\n'
    files[root / pkg / 'models.py'] = f'''from dataclasses import dataclass
from typing import Optional

@dataclass
class {pkg_name}Record:
    id: int
    project_id: Optional[int] = None
    source_reference: Optional[str] = None
    confidence: Optional[float] = None
    review_status: Optional[str] = None
'''
    files[root / pkg / 'schemas.py'] = f'''from typing import Optional
from pydantic import BaseModel

class {pkg_name}Request(BaseModel):
    project_id: Optional[int] = None
    source_reference: Optional[str] = None

class {pkg_name}Response(BaseModel):
    id: int
    status: str
    message: Optional[str] = None
'''
    files[root / pkg / 'service.py'] = f'''from typing import Any, Dict

class {pkg_name}Service:
    def __init__(self) -> None:
        pass

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {{'status': 'ok', 'payload': payload}}
'''
    files[root / pkg / 'router.py'] = f'''from fastapi import APIRouter
from .schemas import {pkg_name}Response

router = APIRouter(prefix='/{pkg}', tags=['ai_smeta_ru'])

@router.get('/health', response_model={pkg_name}Response)
def health() -> {pkg_name}Response:
    return {pkg_name}Response(id=0, status='healthy')
'''
    files[root / pkg / 'README.md'] = f'''# {pkg.replace('_', ' ').title()}

## Purpose

This package is a skeleton for the `{pkg}` subcomponent of `ai_smeta_ru`.

## Responsibilities

- Placeholder models and schemas
- Placeholder service class for processing
- Placeholder router and endpoints

## TODO

- implement domain-specific models
- implement service methods
- implement router endpoints
- wire the component into the `ai_smeta_ru` module
'''

for path, content in files.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

Task = Path('docs/tasks/TASK_002_AI_SMETA_MODULE_SKELETON.md')
Task.parent.mkdir(parents=True, exist_ok=True)
Task.write_text('''# TASK 002 — AI-Smeta-RU Module Skeleton

## What was created

- `backend/app/modules/ai_smeta_ru/`
- `backend/app/modules/ai_smeta_ru/common/`
- `backend/app/modules/ai_smeta_ru/document_understanding/`
- `backend/app/modules/ai_smeta_ru/quantity_normalization/`
- `backend/app/modules/ai_smeta_ru/completeness_checker/`
- `backend/app/modules/ai_smeta_ru/designer_questions/`
- `backend/app/modules/ai_smeta_ru/assumption_engine/`
- `backend/app/modules/ai_smeta_ru/standards_mapping/`
- `backend/app/modules/ai_smeta_ru/pre_expertise_self_check/`
- `backend/app/modules/ai_smeta_ru/grandsmeta_excel_export/`
- `backend/app/modules/ai_smeta_ru/estimator_package/`

Each subpackage contains:
- `__init__.py`
- `models.py`
- `schemas.py`
- `service.py`
- `router.py`
- `README.md`

## Common package

The common package contains base models, enums, constants, and provenance definitions.

## Next steps / TODO

- implement concrete business logic in each service
- wire subpackage routers into application routing
- add module registration and manifest integration if needed
- create data persistence and migration support later
- implement end-to-end AI extraction, normalization, and GrandSmeta export behavior
''', encoding='utf-8')
print('created skeleton')
